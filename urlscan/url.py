# _*_ coding:utf-8 _*_
import urllib2

url = "http://www.baidu.com/"

headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
headers['Host'] = 'www.baidu.com'

#传入URL跟请求头
request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)


print response.read()
response.close()