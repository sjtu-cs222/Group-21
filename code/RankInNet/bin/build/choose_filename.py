
filename_set=set()
f=open('MQ2007/Fold1/train.txt','r')
f2=open('MQ2007/Fold1/test.txt','r')
f3=open('MQ2007/Fold1/vali.txt','r')

for line in f:
	doc_name=line.split('#')[-1].split(' inc')[0]
	filename_set.add(doc_name)
for line in f2:
	doc_name=line.split('#')[-1].split(' inc')[0]
	filename_set.add(doc_name)
for line in f3:
	doc_name=line.split('#')[-1].split(' inc')[0]
	filename_set.add(doc_name)

filename_file=open('MQ2007/Fold1/train_name.txt','w')
for i in filename_set:
	filename_file.writelines(i+'\n')