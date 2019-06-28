#coding:utf-8
#第10章，文件读取和异常处理
filename='pi_digits.txt'
with open(filename) as file_object:
    #for link in file_object:
        #print link.rstrip()
    #print '123'
    lines=file_object.readlines()
    #print contents.rstrip()
pi_string=''
for line in lines:
    pi_string   +=  line.rstrip()
print pi_string
print len(pi_string)

#for link in links:
    #print link.rstrip()
