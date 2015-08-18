#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name: momentum.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

from WindPy import *
from datetime import *
import numpy as np
import matplotlib.pyplot as plt

def test(stock_name_list):

	if w.isconnected() == False:
		w.start()

	
	for stock_name in stock_name_list:
		f = open(stock_name,"w")
		data = w.wsi(stock_name,"close","2001-01-01",datetime.today(),BarSize=60,showblank=0)

		for ii in range(len(data.Times)):
			f.write(str(data.Times[ii])+"   " + str(data.Data[0][ii]))
			f.write("\n")

		f.close()


def load_data(stock_name_list):

	stock_data_list = []
	data_time_list  = []

	if w.isconnected() == False:
		w.start()

	for ii in range(len(stock_name_list)):
		
		temp_data = w.wsi(stock_name_list[ii],"close","2001-01-01",datetime.today(),BarSize = 60,showblank =0)

		#temp_data = w.wsd(stock_name_list[ii], "close","20000101", "","PriceAdj=F",showblank=0)
		

		temp_data_list = []
		for jj in range(len(temp_data.Data[0])):
			if float(temp_data.Data[0][jj])!=0:
				temp_data_list.append(float(temp_data.Data[0][jj]))
			
		stock_data_list.append(temp_data_list)
		data_time_list.append(temp_data.Times)

	return stock_data_list,data_time_list

#做空
def strategy(stock_data_list,stock_compare_time = 4):

	strategy_return = []
	action_type_list = []
	action_time_list = []
	action_point_list = []

	trade_cost = 1-0.0005

	for ii in range(len(stock_data_list)):

		# 0空仓，1 long，-1 short
		pos_flag = 0
		action_flag = ""

		temp_action_type_list = []
		temp_action_time_list = []
		temp_return = []
		temp_action_point_list = []

		for jj in range(stock_compare_time,len(stock_data_list[ii])):
			if stock_data_list[ii][jj] >= stock_data_list[ii][jj-stock_compare_time]:
				if pos_flag !=1:

					# return 
					if pos_flag ==0:
						for kk in range(jj):
							temp_return.append(stock_data_list[ii][jj])
					else:
						temp_return.append(trade_cost*temp_return[-1]*(2-stock_data_list[ii][jj]/stock_data_list[ii][jj-1]))

					temp_action_type_list.append("b")
					temp_action_time_list.append(jj)
					temp_action_point_list.append(stock_data_list[ii][jj])
					pos_flag =1 
				else:
					temp_return.append(temp_return[-1]*(stock_data_list[ii][jj]/stock_data_list[ii][jj-1]))

			else:
				if pos_flag != -1:

					if pos_flag ==0:
						for kk in range(jj):
							temp_return.append(stock_data_list[ii][jj])
					else:
						temp_return.append(trade_cost*temp_return[-1]*(stock_data_list[ii][jj]/stock_data_list[ii][jj-1]))

					temp_action_type_list.append("s")
					temp_action_time_list.append(jj)
					temp_action_point_list.append(stock_data_list[ii][jj])
					pos_flag =-1

				else:
					temp_return.append(temp_return[-1]*(2-stock_data_list[ii][jj]/stock_data_list[ii][jj-1]))

		action_type_list.append(temp_action_type_list)
		action_time_list.append(temp_action_time_list)
		action_point_list.append(temp_action_point_list)
		strategy_return.append(temp_return)

	action_info = []

	for ii in range(len(action_type_list)):
		long_index_list = []
		short_index_list = []
		long_point_list = []
		short_point_list = []
		temp_action_info = []
		for jj in range(len(action_type_list[ii])):
			if action_type_list[ii][jj] =="b":
				long_index_list.append(action_time_list[ii][jj])
				long_point_list.append(action_point_list[ii][jj])
			elif action_type_list[ii][jj] =="s":
				short_index_list.append(action_time_list[ii][jj])
				short_point_list.append(action_point_list[ii][jj])
			else:
				print "type wrong!"
		temp_action_info.append(long_index_list)
		temp_action_info.append(long_point_list)
		temp_action_info.append(short_index_list)
		temp_action_info.append(short_point_list)
		action_info.append(temp_action_info)


	return strategy_return,action_info

# 空仓
def new_strategy(stock_data_list,stock_compare_time = 4):

	strategy_return = []
	action_type_list = []
	action_time_list = []
	action_point_list = []

	trade_cost = 1-0.0005

	for ii in range(len(stock_data_list)):

		# 0空仓，1 long
		pos_flag = -1
		action_flag = ""

		temp_action_type_list = []
		temp_action_time_list = []
		temp_return = []
		temp_action_point_list = []

		for jj in range(stock_compare_time,len(stock_data_list[ii])):
			if stock_data_list[ii][jj] >= stock_data_list[ii][jj-stock_compare_time]:
				if pos_flag != 1:
					# return 
					if pos_flag ==-1:
						for kk in range(jj):
							temp_return.append(stock_data_list[ii][jj])
					else:
						temp_return.append(trade_cost*temp_return[-1])

					pos_flag = 1
				else:
					temp_return.append(temp_return[-1]*(stock_data_list[ii][jj]/stock_data_list[ii][jj-1]))

			else:
				if pos_flag == 1:
					temp_return.append(trade_cost*temp_return[-1]*(stock_data_list[ii][jj]/stock_data_list[ii][jj-1]))
					pos_flag = 0

				elif pos_flag ==0:
					temp_return.append(temp_return[-1])

		strategy_return.append(temp_return)


	return strategy_return

if __name__ == '__main__':

	stock_name_list = ["IC.CFE","IF00.CFE"]
	test(stock_name_list)
	stock_compare_time = 4

	stock_data_list,data_time_list = load_data(stock_name_list)
	strategy_return,action_info_list = strategy(stock_data_list)
	new_strategy_return = new_strategy(stock_data_list)


	for ii in range(len(stock_name_list)):
		figure_name = stock_name_list[ii]
		plt.figure(figure_name)

		print len(action_info_list[ii][0])+len(action_info_list[ii][2])

		plt.plot(strategy_return[ii],"r")
		plt.plot(new_strategy_return[ii],"k")
		plt.scatter(action_info_list[ii][0],action_info_list[ii][1],c="k",s=50)
		plt.scatter(action_info_list[ii][2],action_info_list[ii][3],c="r",s=50)
		plt.plot(stock_data_list[ii],"b")

		plt.xlabel("Time /day")
		plt.ylabel("Stock Price")
		plt.grid(True)


	plt.show()

