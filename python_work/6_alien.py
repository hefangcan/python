#coding:utf-8
#第六章 字典的使用，其实我感觉就是JSON格式
alien_0 = {'coloer':'green','points':5}
new_points=alien_0['points']
print "你有"+str(new_points)+"积分"

alien_0['x_position']   =   0
alien_0['y_position']   =   25
print alien_0

del alien_0['points']
print alien_0

favrite_languages = {
    'jen':'python',
    'sarah':'c',
    'edward':'ruby',
    'phil':'python',
    }
print favrite_languages['sarah'].title()

for key,value in favrite_languages.items():
    print key
    print value
    
#下面之输出建的内容。值的内容不提取
for name in favrite_languages.keys():
    print name

#只输出值内容用关键字values,set表示提取不种复内容
for languages in set(favrite_languages.values()):
    print languages
    

