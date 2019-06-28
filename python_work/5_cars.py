#coding:utf-8
#第5章，IF语句
cars=['audi','bmw','subaru','toyata']
user="subaru"
for car in cars:
    if car=='bmw':
        print car.upper()
    else:
        print car.title()

#检查user是否包在cars
print user in cars
#检查user是否不包含在cars
print user not in cars

age=18
if age>=18:
    print "you are old enough to vote!"
else:
    print "sorry,you are too young to vote"

#amusenment_park.py
age=12
if age<4:
    price=0
elif age < 18:
   price=5
else:
    price=10
print "your cost is $"+str(price)

requested_toppings=['mushrooms','green peppers','extra cheese']
for requested_topping in requested_toppings:
    if requested_topping == 'green peppers':
        print "sorry,we are out of green peppers right now."
    else:
        print "Adding "+requested_topping
print "\nFinished making you pizza"











