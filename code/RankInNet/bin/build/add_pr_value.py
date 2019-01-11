
f1=open('MQ2007/Fold1/test.txt','r')
res1=open('MQ2007/Fold1/test_pr.txt','w')
f2=open('MQ2007/Fold1/train.txt','r')
res2=open('MQ2007/Fold1/train_pr.txt','w')
f3=open('MQ2007/Fold1/vali.txt','r')
res3=open('MQ2007/Fold1/vali_pr.txt','w')

for line in f1:
	para_list = line.split(' ')
	para_list=para_list[:22]+para_list[42:45]+[para_list[47]]+para_list[48:]
	#print para_list
	for i in para_list:
		if i[-1]!='\n':
			res1.write(i+' ')
		else:
			res1.write(i)

for line in f2:
	para_list = line.split(' ')
	para_list = para_list[:22] + para_list[42:45] + [para_list[47]] + para_list[48:]
	for i in para_list:
		if i[-1]!='\n':
			res2.write(i+' ')
		else:
			res2.write(i)

for line in f3:
	para_list = line.split(' ')
	para_list = para_list[:22] + para_list[42:45] + [para_list[47]] + para_list[48:]
	for i in para_list:
		if i[-1]!='\n':
			res3.write(i+' ')
		else:
			res3.write(i)

