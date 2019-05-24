#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 11:22:09 2019

@author: linxier
"""


import json




def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


with open("/Users/linxier/vivosession.json") as f:
    data = f.readlines()
json_data_list=[]
comment={}
comment_data=[]
#data = json.load(json_data)
#去除非json对象
for line in data:
    if(is_json(line)):
        json_data_list.append(json.loads(line))
    else:
        pass

app_name_list=[]
comment_index=[]
for json_data in json_data_list:
    if ("comment" in json_data.keys()):
        index=json_data_list.index(json_data)
        comment_index.append(index)
    else:
        pass
#print(comment_index)
count=len(comment_index)
#print(count)
i=0

for json_data in json_data_list:
    if ("comment" in json_data.keys()):
        app_name=json_data["value"]["title_zh"]

        f=open("/Users/linxier/vivocomment_%s.json"%app_name,"w")
        f.truncate()
        f.close()
        for json_data in json_data_list[comment_index[i]:comment_index[i+1] if (i+1)<count else -1]:
            if ("value" in json_data.keys()):
                try:
                    for value_data in json_data["value"]:

                        comment_dic={}
                        comment_dic["date"]=value_data["comment_date"]
                        comment_dic["version"]=value_data["appversion"]
                        comment_dic["comment"]=value_data["comment"]
                        comment_dic["score"]=value_data["score"]
                        comment_dic["device"]=value_data["model"]
                        comment_dic["user"]=value_data["user_name"]
                        #comment[app_name].append(comment_dic)
                        with open("/Users/linxier/vivocomment_%s.json"%app_name,"a") as f_out:
                            out_data = json.dumps(comment_dic,ensure_ascii=False,indent=2)
                            f_out.write(out_data)
                except:
                    pass
            else:
                pass
        i=i+1
        if(i==count):
            break
    else:
        pass
    

