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

def get_extreme_high_point(price_high):
    compared_day = 3
    extreme_high_point = []
    extreme_high_point_index = []
    price_high_new= []
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

    return extreme_high_point,extreme_high_point_index

def get_extreme_low_point(price_low):
    compared_day = 3
    extreme_low_point = []
    extreme_low_point_index = []
    price_low_new= []
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

    return extreme_low_point,extreme_low_point_index


if __name__  == "__main__":
    filename = "shcomp_data.xlsx"
    stock_date,price_high,price_low,stock_volume,price_closed = load_data(filename)

    #得到极大值点
    extreme_high_point,extreme_high_point_index = get_extreme_high_point(price_high)

    extreme_low_point, extreme_low_point_index = get_extreme_low_point(price_low)

    
    plt.plot(price_high)
    plt.plot(extreme_high_point_index,extreme_high_point,"r+",linewidth=5)
    plt.plot(price_low,"g")
    plt.plot(extreme_low_point_index,extreme_low_point,"b+",linewidth=5)


    plt.grid(True)
    plt.xlabel("Time(day)")
    plt.ylabel("price")
    plt.title("High Price")
    plt.show()