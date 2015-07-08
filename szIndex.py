#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name: szIndex.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

import os
from openpyxl.reader.excel import load_workbook
import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    wb = load_workbook(filename)
    sheetnames = wb.get_sheet_names()
    ws = wb.get_sheet_by_name(sheetnames[0])
    stock_date = []
    price_high = []
    price_low = []
    stock_volume = []
    price_closed = []
    for rx in range(5,ws.get_highest_row()+1):
        stock_date.append(ws.cell(row =rx ,column = 1).value)
        price_high.append(ws.cell(row=rx,column=2).value)
        price_low.append(ws.cell(row=rx,column=3).value)
        stock_volume.append(ws.cell(row=rx,column=4).value)
        price_closed.append(ws.cell(row=rx,column=5).value)

    return stock_date,price_high,price_low,stock_volume,price_closed

def get_extreme_high_point(price_high,compared_day):

    extreme_high_point = []
    extreme_high_point_index = []
    price_high_new= []
    high_point =[]
    high_point_index = []
    sell_point = []
    sell_point_index = []
    #新数组
    for i in range(compared_day):
        price_high_new.append(price_high[0])

    for i in range(len(price_high)):
        price_high_new.append(price_high[i])

    for i in range(compared_day):
        price_high_new.append(price_high[len(price_high)-1])


    for i in range(len(price_high)):
        flag =1
        for j in range(compared_day*2+1):
            if price_high_new[i+compared_day]< price_high_new[i+j]:
                flag = 0
                break
        if flag == 1:
            extreme_high_point_index.append(i)
            extreme_high_point.append(price_high[i])

    for i in range(len(extreme_high_point)-1):
        flag =1
        if i < compared_day:
            continue
        else:
            for j in range(compared_day):
                if extreme_high_point[i-j-1]>extreme_high_point[i]:
                    flag=1
                    break
                else:
                    flag=flag+1
                if flag == compared_day+1:
                    if extreme_high_point[i+1]<extreme_high_point[i]:
                        high_point.append(extreme_high_point[i])
                        high_point_index.append(extreme_high_point_index[i])
                        sell_point.append(extreme_high_point[i+1])
                        sell_point_index.append(extreme_high_point_index[i+1])

    return high_point,high_point_index,sell_point,sell_point_index

    #return extreme_high_point,extreme_high_point_index

def get_extreme_low_point(price_low,compared_day):
    extreme_low_point = []
    extreme_low_point_index = []
    price_low_new= []
    low_point =[]
    low_point_index =[]
    buy_point =[]
    buy_point_index =[]
    #新数组
    for i in range(compared_day):
        price_low_new.append(price_low[0])

    for i in range(len(price_low)):
        price_low_new.append(price_low[i])

    for i in range(compared_day):
        price_low_new.append(price_low[len(price_low)-1])


    for i in range(len(price_low)):
        flag =1
        for j in range(compared_day*2+1):
            if price_low_new[i+compared_day]> price_low_new[i+j]:
                flag = 0
                break
        if flag == 1:
            extreme_low_point_index.append(i)
            extreme_low_point.append(price_low[i])

    for i in range(len(extreme_low_point)-1):
        flag =1
        if i < compared_day:
             continue
        else:
            for j in range(compared_day):
                if extreme_low_point[i-j-1]<extreme_low_point[i]:
                    flag =1
                    break
                else:
                    flag =flag+1
                if flag ==compared_day+1:
                    #反弹条件
                    if extreme_low_point[i+1]>extreme_low_point[i]:
                        low_point.append(extreme_low_point[i])
                        low_point_index.append(extreme_low_point_index[i])
                        buy_point.append(extreme_low_point[i+1])
                        buy_point_index.append(extreme_low_point_index[i+1])

    return low_point,low_point_index,buy_point,buy_point_index
    #return extreme_low_point,extreme_low_point_index

#合并两个数组
def mix_signal_array(high_point_index,low_point_index):
    temp_high_index = 0
    temp_low_index  = 0
    mix_index = []
    mix_signal = []
    for i in range(len(high_point_index)+len(low_point_index)):

        if temp_high_index<len(high_point_index) and temp_low_index<len(low_point_index):
            if  high_point_index[temp_high_index]<low_point_index[temp_low_index]:
                mix_index.append(high_point_index[temp_high_index])
                temp_high_index = temp_high_index+1
                mix_signal.append('s')
            elif high_point_index[temp_high_index]>low_point_index[temp_low_index]:
                mix_index.append(low_point_index[temp_low_index])
                temp_low_index = temp_low_index+1
                mix_signal.append('b')
            else:
                # 如果同一天两个指标同时出现，则舍弃
                temp_low_index = temp_low_index+1
                temp_high_index = temp_high_index+1
                i = i+1
        elif temp_high_index ==len(high_point_index) and temp_low_index<len(low_point_index):
            mix_index.append(low_point_index[temp_low_index])
            mix_signal.append('b')
            temp_low_index = temp_low_index+1
        elif temp_high_index <len(high_point_index) and temp_low_index==len(low_point_index):
             mix_index.append(high_point_index[temp_high_index])
             temp_high_index = temp_high_index+1
             mix_signal.append('s')

    return mix_index,mix_signal

#计算收益率
def cal_revenue(price_closed,mix_index,mix_signal):

    flag =0
    new_index = []
    new_signal = []
    for i in range(len(mix_index)):
        if mix_signal[i]=='b':
            if flag==0:
                flag=1
                new_index.append(mix_index[i])
                new_signal.append(mix_signal[i])
        else:
            if flag==1:
                new_index.append(mix_index[i])
                new_signal.append(mix_signal[i])
                flag =0
    flag =0
    revenue = []
    action_index =0
    #base 上一日的资产
    base =100
    for i in range(len(price_closed)):
        #前一天是空仓
        if flag ==0:
            if i ==new_index[action_index] and new_signal[action_index] =='b':
                revenue.append(base)
                flag =1
                action_index =action_index+1
                if action_index == len(new_index):
                    action_index = action_index-1
            else:
                revenue.append(base)

        #前一天有仓位
        else:
            if i == new_index[action_index] and new_signal[action_index]=='s':
                base = base*price_closed[i]/price_closed[i-1]
                flag=0
                action_index =action_index+1
                if action_index == len(new_index):
                    action_index =action_index-1
                revenue.append(base)
            #继续持仓
            else:
                base = base*price_closed[i]/price_closed[i-1]
                revenue.append(base)



    return revenue,new_index,new_signal



if __name__  == "__main__":
    filename = "shcomp_data.xlsx"
    #比较的时间长度
    compared_day = 2
    stock_date,price_high,price_low,stock_volume,price_closed = load_data(filename)


    #得到极大值点
    extreme_high_point,extreme_high_point_index,sell_point,sell_point_index = get_extreme_high_point(price_high,compared_day)

    extreme_low_point, extreme_low_point_index,buy_point,buy_point_index = get_extreme_low_point(price_low,compared_day)

    mix_index,mix_signal = mix_signal_array(sell_point_index,buy_point_index)

    revenue,new_index,new_signal = cal_revenue(price_closed,mix_index,mix_signal)


    # output =open('data.txt','w')
    # output.write("High Point:\n \n")
    # for i in range(len(extreme_high_point)):
    #     output.write(str(extreme_high_point_index[i]))
    #     output.write("\n")
    # output.write("\n Low Point:\n\n")
    # for i in range(len(extreme_low_point_index)):
    #     output.write(str(extreme_low_point_index[i]))
    #     output.write("\n")
    #
    # output.close()

    output = open('data.txt','w')
    output.write("result:\n")
    for i in range(len(revenue)):
        output.write(str(revenue[i]))
        output.write("\n")
    output.close()

    plt.plot(price_high)
    plt.plot(extreme_high_point_index,extreme_high_point,"r+",linewidth=5)
    plt.plot(price_low,"g")
    plt.plot(extreme_low_point_index,extreme_low_point,"b+",linewidth=5)

    plt.plot(revenue,"y")



    plt.grid(True)
    plt.xlabel("Time(day)")
    plt.ylabel("price")
    plt.title("High Price")
    plt.show()