#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 14:28:28 2019

@author: linxier
"""

import json

def is_alphabet(uchar):
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False
    
with open("/Users/linxier/opposession.json") as f:
    oppo_data = f.readlines()

app_exist='com.oppo.cdo.detail.domain.dto.detail.BaseDetailDto\n'
app_index=[]

for data in oppo_data:
    if(data==app_exist):
        index=oppo_data.index(data)+1
        oppo_data[index-1]=''
        app_index.append(index)
    else:
        pass

comment={}
comment_exist='com.oppo.cdo.common.domain.dto.comment.CommentDto\n'
count=len(app_index)

i=0
while(i<(count)):
    app_name=oppo_data[app_index[i]].strip('\n')
    f=open("/Users/linxier/oppocomment_%s.json"%app_name,"w")
    f.truncate()
    f.close()
    for data in oppo_data[app_index[i]:app_index[i+1] if (i+1)<count else -1]:
        if(data==comment_exist):
            for num in range(3,10):
                if(is_alphabet(oppo_data[oppo_data.index(data)+num][0])&is_alphabet(oppo_data[oppo_data.index(data)+num][1])):
                    device_index_num=oppo_data.index(data)+num
                    break
            comment_index=oppo_data.index(data)+1
            comment_dic={}
            comment_dic["comment"]=''
            for comment_num in range(comment_index,device_index_num-1):
                comment_dic["comment"]=comment_dic["comment"]+' '+oppo_data[comment_num].strip('\n')
            user_index=device_index_num-1
            device_index=device_index_num
            
            
            comment_dic["user"]=oppo_data[user_index].strip('\n')
            comment_dic["device"]=oppo_data[device_index].strip('\n')
            comment_dic["date"]=None
            comment_dic["score"]=None
            comment_dic["version"]=None
            #comment[app_name].append(comment_dic)
            with open("/Users/linxier/oppocomment_%s.json"%app_name,"a") as f_out:
                out_data = json.dumps(comment_dic,ensure_ascii=False,indent=2)
                f_out.write(out_data)
            oppo_data[comment_index-1]=''
        else:
            pass
    i=i+1

