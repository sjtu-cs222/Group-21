import collections

import numpy as np
from chainer.datasets import TupleDataset


class DatsetParseError(Exception):
    pass


def _parse_single(line):
    data = line.strip().split()[:26]
    rank = int(data[0])
    qid = int(data[1][4:])
    val = map(lambda x: float(x.split(':')[1]), data[2:])
    return qid, rank, val

class DatasetParseError(RuntimeError):
    def __init__(self, arg):
        self.args = arg

def create_dataset(path, size=-1):

    data = collections.defaultdict(lambda: [[], []])
    with open(path, mode='r') as fin:
        for i, line in enumerate(fin):
            q, r, v = _parse_single(line)
            if r not in {0, 1, 2}:
                raise DatasetParseError(
                    "L%d: Score must be 0, 1 or 2, but found %d" %
                    (i, r)
                )
            data[q][0].append(r)
            data[q][1].append(v)
    vectors = []
    scores = []
    for d in data.values():
        v = np.array(d[1], dtype=np.float32)
        s = np.array(d[0], dtype=np.float32)
        vectors.append(v)
        scores.append(s)
    s = max(map(len, scores))
    vectors_pad = np.zeros((len(vectors), s, v.shape[-1]), dtype=np.float32)
    scores_pad = np.zeros((len(scores), s), dtype=np.float32)
    length = np.empty((len(scores)), dtype=np.int32)
    for i, (s, v) in enumerate(zip(scores, vectors)):
        vectors_pad[i, :len(v), :] = v
        scores_pad[i, :len(s)] = s
        length[i] = len(v)

    if size > 0:
        ind = np.random.permutation(len(vectors))[:size]
        return TupleDataset(vectors_pad[ind], scores_pad[ind], length[ind])
    else:
        return TupleDataset(vectors_pad, scores_pad, length)
