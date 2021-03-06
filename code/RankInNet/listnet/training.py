import logging

import chainer
import chainer.functions as F
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('gbk')
import matplotlib.pyplot as plt

def mean_average_precision(probs, labels, length, th):

    num_queries = len(probs)
    out = 0.0

    for i in xrange(len(probs)):
        r = probs[i][:length[i]].argsort()
        r = r[::-1]
        candidates = labels[i, r]
        avg_prec = 0.
        precisions = []
        num_correct = 0.
        for i in xrange(min(th, len(candidates))):
            if candidates[i] >= 1:
                num_correct += 1
                precisions.append(num_correct / (i + 1))

        if precisions:
            avg_prec = sum(precisions) / len(precisions)

            out += avg_prec
    return out / float(num_queries)


def logsumexp(x, mask, zero_pad, axis):
    x_exp = F.where(mask, F.exp(x), zero_pad)
    return F.log(F.sum(x_exp, axis=axis))


def logsoftmax_no_mask(x, mask, zero_pad, axis):
    x_logsumexp = logsumexp(x, mask, zero_pad, axis)

    return x - F.broadcast_to(F.expand_dims(x_logsumexp, 1), x.shape)


def logsoftmax(x, mask, zero_pad, axis):
    return F.where(mask, logsoftmax_no_mask(x, mask, zero_pad, axis), zero_pad)


def softmax(x, mask, zero_pad, axis):
    x_explogsoftmax = F.exp(logsoftmax_no_mask(x, mask, zero_pad, axis))
    return F.where(mask, x_explogsoftmax, zero_pad)



def permutation_probability_loss(x, t, length):

    length = length.reshape(-1, 1)
    mask = np.tile(np.arange(x.shape[1]).reshape(1, -1), (x.shape[0],  1)) < length
    mask = chainer.Variable(mask)
    padding = chainer.Variable(np.zeros(x.shape, dtype=x.dtype))

    log_p_x = logsoftmax(x, mask, padding, axis=1)
    log_p_t = logsoftmax(t, mask, padding, axis=1)

    loss = F.exp(log_p_t) * log_p_t - F.exp(log_p_t) * log_p_x

    return F.sum(loss) / float(x.shape[0])


def clip_data(x, l):
    return x[:, :max(l)]


def _run_batch(model, optimizer, batch, device, train):
    assert train == (optimizer is not None)
    model.cleargrads()

    x, t, l = chainer.dataset.concat_examples(batch, device=device)
    x = clip_data(x, l)
    t = clip_data(t, l)

    y = model(chainer.Variable(x), train=train)
    loss = permutation_probability_loss(y, chainer.Variable(t), l)
    acc = mean_average_precision(y.data, t, l, 100000)
    if optimizer is not None:
        loss.backward()
        optimizer.update()
    return float(loss.data), acc


def forward_pred(model, dataset, device=None):
    loss = 0.
    acc = 0.
    iterator = chainer.iterators.SerialIterator(dataset, batch_size=4,
                                                repeat=False, shuffle=False)
    for batch in iterator:
        l, a = _run_batch(model, None, batch, device, False)
        loss += l * len(batch)
        acc += a * len(batch)
    return loss / float(len(dataset)), acc / float(len(dataset))


def train(model, optimizer, train_itr, n_epoch, dev=None, device=None,
          tmp_dir='tmp.model', lr_decay=0.995):
    loss = 0.
    acc = 0.
    min_loss = float('inf')
    min_epoch = 0
    report_tmpl = "[{:>3d}] T/loss={:0.6f} T/acc={:0.6f} D/loss={:0.6f} D/acc={:0.6f} lr={:0.6f}"
    train_loss_list=list()
    train_acc_list=list()
    test_loss_list = list()
    test_acc_list = list()
    epoch_list=list()
    for batch in train_itr:
        if train_itr.is_new_epoch:
            loss_dev, acc_dev = forward_pred(model, dev, device=device)
            loss = loss / len(train_itr.dataset)
            acc = acc / len(train_itr.dataset)
            logging.info(report_tmpl.format(
                train_itr.epoch - 1, loss, acc, loss_dev, acc_dev, optimizer.alpha))
            train_loss_list.append(loss)
            train_acc_list.append(acc)
            test_loss_list.append(loss_dev)
            test_acc_list.append(acc_dev)
            epoch_list.append(train_itr.epoch - 1)
            if loss_dev < min_loss:
                min_loss = loss_dev
                min_epoch = train_itr.epoch - 1
                chainer.serializers.save_npz(tmp_dir, model)

            loss = 0.
            acc = 0.
            optimizer.alpha *= lr_decay
        if train_itr.epoch == n_epoch:
            break
        l, a = _run_batch(model, optimizer, batch, device, True)
        loss += l * len(batch)
        acc += a * len(batch)

    logging.info('loading early stopped-model at epoch {}'.format(min_epoch))
    chainer.serializers.load_npz(tmp_dir, model)
    plt.figure(1)
    plt.plot(epoch_list, train_loss_list)
    plt.plot(epoch_list, test_loss_list)
    plt.title("model loss")
    plt.ylabel("loss")
    plt.xlabel("epoch")
    plt.legend(["train", "test"], loc="upper left")
    plt.figure(2)
    plt.plot(epoch_list, train_acc_list)
    plt.plot(epoch_list, test_acc_list)
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", "test"], loc="upper left")
    plt.show()