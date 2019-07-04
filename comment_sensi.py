#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:43:44 2019

@author: linxier
"""

import jieba
import json

def dic_load():
    posdict=[]
    negdict=[]
    mostdict=[]
    verydict=[]
    moredict=[]
    ishdict=[]
    deny_word=[]
    f1 = open('/Users/linxier/sensitive_dic/posdict.txt', 'r')                   #以读方式打开文件
    for line in f1.readlines():                          #依次读取每行
        line = line.strip('\n')                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        posdict.append(line)
    f2 = open('/Users/linxier/sensitive_dic/negdict.txt', 'r')                   #以读方式打开文件
    for line in f2.readlines():                          #依次读取每行
        line = line.strip()                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        negdict.append(line)
    f3 = open('/Users/linxier/sensitive_dic/mostdict.txt', 'r')                   #以读方式打开文件
    for line in f3.readlines():                          #依次读取每行
        line = line.strip()                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        mostdict.append(line)
    f4 = open('/Users/linxier/sensitive_dic/verydict.txt', 'r')                   #以读方式打开文件
    for line in f4.readlines():                          #依次读取每行
        line = line.strip()                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        verydict.append(line)
    f5 = open('/Users/linxier/sensitive_dic/moredict.txt', 'r')                   #以读方式打开文件
    for line in f5.readlines():                          #依次读取每行
        line = line.strip()                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        moredict.append(line)
    f6 = open('/Users/linxier/sensitive_dic/ishdict.txt', 'r')                   #以读方式打开文件
    for line in f6.readlines():                          #依次读取每行
        line = line.strip()                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        ishdict.append(line)
    f7 = open('/Users/linxier/sensitive_dic/deny_word.txt', 'r')                   #以读方式打开文件
    for line in f7.readlines():                          #依次读取每行
        line = line.strip()                             #去掉每行头尾空白
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行
            continue                                    #是的话，跳过不处理
        deny_word.append(line)

    return posdict,negdict,mostdict,verydict,moredict,ishdict,deny_word


def sentiment_score_list(seg_sentence,posdict,negdict,mostdict,verydict,moredict,ishdict,deny_word):

    sen_dic={}
    jieba.load_userdict('/Users/linxier/userdict.txt')
    for sen in seg_sentence: #循环遍历每一个评论
        segtmp = jieba.lcut(sen, cut_all=False)  #把句子进行分词，以列表的形式返回
        i = 0 #记录扫描到的词的位置
         #记录情感词的位置
        sen_count=0
        poscount = 0 #积极词的第一次分值
        pos_count = 0 #积极词反转后的分值

        negcount = 0
        neg_count = 0

        for word in segtmp:
            a = max(i-3,0)
            if word in posdict:  # 判断词语是否是情感词
                print(word)
                poscount += 1
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    if w in mostdict:
                        poscount *= 2.0
                    elif w in verydict:
                        poscount *= 1.5
                    elif w in moredict:
                        poscount *= 1.0
                    elif w in ishdict:
                        poscount *= 0.5
                    elif w in deny_word:
                        c += 1
                #if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                if c%2 == 1:
                    poscount *= -1.0
                    pos_count += poscount
                    poscount = 0

                else:
                    pos_count = poscount + pos_count
                    poscount = 0
                a = i + 1  # 情感词的位置变化
 
            elif word in negdict:  # 消极情感的分析，与上面一致
                print(word)
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in mostdict:
                        negcount *= 4.0
                    elif w in verydict:
                        negcount *= 3.0
                    elif w in moredict:
                        negcount *= 2.0
                    elif w in ishdict:
                        negcount *= 0.5
                    elif w in deny_word:
                        d += 1
                if d%2 == 1:
                    negcount *= -1.0
                    neg_count += negcount
                    negcount = 0
                else:
                    neg_count = negcount + neg_count
                    negcount = 0
                a = i + 1

            i += 1 # 扫描词位置前移

        sen_count=pos_count-neg_count
        if sen_count>5:
            sen_count=5
        elif sen_count<-5:
            sen_count=-5
        sen_dic[sen]=sen_count
        #print(pos_count)
        #print(neg_count)
        #print(sen)
        #print(sen_count)
    return sen_dic
 

comment_list=[]            
with open('/Users/linxier/vivocomment_西瓜视频.json') as reader:
    for index, line in enumerate(reader):
        if index % 7 == 3:
            comment_list.append(line.strip(' "comment": ",\n'))
#print(comment_list)
posdict,negdict,mostdict,verydict,moredict,ishdict,deny_word=dic_load()

sen_dic=sentiment_score_list(comment_list,posdict,negdict,mostdict,verydict,moredict,ishdict,deny_word)
print(json.dumps(sen_dic,ensure_ascii=False,indent=2))
with open("/Users/linxier/comment_sen.json",'a') as f_out:
    out_data = json.dumps(sen_dic,ensure_ascii=False,indent=2)
    f_out.write(out_data)
#data1= ['垃圾软件，越做越垃圾之前还能看电影，现在电影都看不了，一星就不给']
#print(sentiment_score_list(data1,posdict,negdict,mostdict,verydict,moredict,ishdict,deny_word))

