#-*- coding:utf-8 -*-
import sys,os

with open('ans.test') as f:
    ans = f.readlines()
    
with open('ans.test2') as f:
    myans = f.readlines()

count = 0
hits = 0.0
for i in ans:
    if i == myans[count]:
        hits +=1
        #print ans[count], myans[count]
    count +=1

print 'hit/count = ', hits/count
