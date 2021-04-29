from django.shortcuts import render
import csv
import os
from django.http import HttpResponse
from main_app.models import UserFoodItems
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from math import sqrt
# Create your views here.

@login_required(login_url='login')
def export(request):
    with open('static/userdata/userdata.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
        fieldnames = ['userid','foodname','count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for food in UserFoodItems.objects.all():
            writer.writerow({'userid':food.userid, 'foodname':food.name, 'count':food.quantity})
        print(food.user)
    return render(request, 'suggest/create.html')

Food = pd.read_csv("static/userdata/통합 식품영양성분DB_333.csv")
user = pd.read_csv("static/userdata/userdata.csv")
foods = Food.loc[:,('NO','식품명')]
user = user.rename(columns = {'foodname':'식품명'})
users = pd.merge(user, foods, on='식품명')
data=pd.merge(Food,users,on="NO")
column=['userid','NO','count']
data=data[column]

fooddata=data.pivot_table(index='userid',  columns="NO")['count']
fooddata.fillna(-1, inplace=True)

def sim_pearson(data, n1, n2):
    sumX=0
    sumY=0
    sumSqX=0 # x 제곱합
    sumSqY=0 # y 제곱합
    sumXY=0 #XY 합
    cnt =0 #음식 먹은 횟수
    for i in data.loc[n1,data.loc[n1,:]>=0].index:
        if  data.loc[n2,i]>=0:
            sumX+=data.loc[n1,i]
            sumY+=data.loc[n2,i]
            sumSqX+=pow(data.loc[n1,i],2)
            sumSqY+=pow(data.loc[n2,i],2)
            sumXY+=(data.loc[n1,i])*(data.loc[n2,i])
            cnt+=1
            global num
            global den
            num=sumXY-((sumX*sumY)/cnt)
            den= (sumSqX-(pow(sumX,2)/cnt))*(sumSqY-(pow(sumY,2)/cnt))
    return num/sqrt(den+0.00001) # 분모=0방지

def top_match(data, name, rank = 5, simf = sim_pearson):
    simList = []
    for i in data.index:
        if name != i:
            if simf(data, name, i) is not None:
                simList.append((simf(data, name, i), i))
    simList.sort()
    simList.reverse()
    return simList[:rank]


def recommendation(data, person, simf=sim_pearson):
    res = top_match(data, person, len(data))
    score_dic = {}
    sim_dic = {}
    myList = []
    for sim, name in res:
        if sim < 0:
            continue
        for food in data.loc[person, data.loc[person, :] < 0].index:
            simSum = 0
            if data.loc[name, food] >= 0:
                simSum += sim * data.loc[name, food]

                score_dic.setdefault(food, 0)
                score_dic[food] += simSum

                sim_dic.setdefault(food, 0)
                sim_dic[food] += sim
    for key in score_dic:
        myList.append((score_dic[key] / sim_dic[key], key))
    myList.sort()
    myList.reverse()

    return myList
def recomomandlist(request):
    List = []
    userid = request.user.id
    for rate, m_id in recommendation(fooddata, userid): #(숫자)고객 번호
        List.append((Food.loc[Food['NO'] == m_id, '식품명'].values[0]))
        if len(List)==5: #유사도 탑 5개까지
            break
    recom = List[:4]
    suggest = {'suggest':recom}
    return render(request, 'suggest/suggestlist.html', suggest)