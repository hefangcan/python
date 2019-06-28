#coding:utf-8
#第8章，函数
#def greet_user(username):
	#print "Hello,"+username.title()
#greet_user("hfc")

 #第9章，类
class Dog(object):
	 #""创建一个小狗类""
	 def __init__(self,name,age):
		 self.name=name
		 self.age=age
	 def sit(self):
		 print self.name.title()+" is now sitting."
	 def roll_over(self):
		 print self.name.title()+"is rolled over!."

my_dog =Dog('duoduo',1)
#print my_dog.name
my_dog.sit()
my_dog.roll_over()

class Mydog(Dog):
	def __init__(self,name,age):
		super(Mydog,self).__init__(name,age)

testdog=Mydog('fuck',2)
testdog.sit()
