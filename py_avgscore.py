#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 11:29:56 2019

@author: linxier
"""

import numpy as np
import matplotlib.pyplot as plt
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.comment
collection = db.douyin

pipeline=[{'$match':{'date':{'$gt':'2019-04-01 00:00:00'}}},{'$project' : { 'day' : {'$substr': ["$date", 0, 10] },'score':'$score'}},{'$group' : {'_id' : '$day', 'score_avg' : {'$avg' : '$score'}}},{'$sort':{"_id":1}}]

date=[]
score_avg=[]
day_avg=collection.aggregate(pipeline)
for i in day_avg:
    date.append(i['_id'][5:10])
    score_avg.append(i['score_avg'])
    
print(date)
print(score_avg)

 #创建绘图对象
plt.plot(date,score_avg,"b-",linewidth=1)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
plt.xlabel("date-2019") #X轴标签
plt.ylabel("score_avg")  #Y轴标签
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.ylim(0,5)
plt.title("抖音") #图标题
plt.show()
