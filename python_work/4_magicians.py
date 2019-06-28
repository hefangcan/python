#coding:utf-8
#第4章 操作列表，或者叫操作数组

#cars =['bwm','audi','toyata','subaru']
#for car in cars:
    #print car.title()+" is great!"
    #print "I want a "+car.title()+"\n"
#print "Think every car!,I just want!"

#4.3 numbers.py
#for value in range(1,6):
    #print value

#numbers=list(range(1,6))
#print numbers

#even_numbers=list(range(2,11,2))
#print even_numbers

#squares=[]
#for value in range(1,11):
    #squares.append(value**2)
#print squares

#print min(squares)
#print max(squares)
#print sum(squares)
##########################列表解析
#squares=[value**2 for value in range(1,11)]
#print squares

#plays=['charles','martina','michael','florence','eli']
#print plays[:3]

#for play in plays[:3]:
    #print play
    
#############################。4。5元组
dimensions=(200,50)
print dimensions[0]
print dimensions[1]
#下面的是错误的
#dimensions[0]=250
#操作元组需重新赋值
dimensions=(300,30)
for dim in dimensions:
    print dim








