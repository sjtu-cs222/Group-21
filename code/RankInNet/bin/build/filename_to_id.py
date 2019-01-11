

f=open('RefTable.txt','r')
name_id=dict()
for line in f:
    id=line.split('\t')[0]
    name=line.split('\t')[1].split(' ')[-1].split('\n')[0]
    name_id[name]=id


f1=open('MQ2007/Fold1/all_file_name.txt','r')
f2=open('MQ2007/Fold1/all_file_id.txt','w')
for line in f1:
    f2.writelines(name_id[line.split('\n')[0].split(' ')[-1]]+'\n')