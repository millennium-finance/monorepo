import data
import shutil
import os
import position as p
import numpy as np
from datetime import datetime
from dateutil import parser as date_parser
import matplotlib.pyplot as plotter
from collections import deque
# import plotly.graph_obj as pgo
from os import path, mkdir
# import print_to_log as printe
import matplotlib.animation as animation
from itertools import count
import pandas as pd
import global_vars as glv
import random
import time
import math
from graph_to_log import graph_btc, graph_btcdwn, create_path_or_do_nothing

def sim():
	
	# Buy function for simple purchases where 100% of the desired account will be used for the transaction
	# input is price and the usd balance - Output is the net quantitiy of the crypto purchased and the price.. for some reason
	def buy(price, balance):
		crypto = balance / price
		fee = 0.0075 * crypto
		net = bitcoin - fee
		return net, price
	
	# Simple sell function using 100% of the remaining balance 
	# input is crypto price and crypto balance - output is net return
	def sell(price, balance):
		usdt = balance * price
		fee = 0.0075 * usdt
		net = usdt - fee
		return net, price
	
	# Grid trading buy function where a line in a "trade_array" determines the quantity of the crypto to be bought
	# input is price, the purchasing wager (determined buy the remaining balance at the time and the momentum in either direction) 
	# and the trade_array for the crypto in question
	# Outputs are net return of crypto, the price it finished the sale at and the trade_number to be used to close the trade
	def buy_grid(price, buy_wager, crypto_trade_array):
		crypto = buy_wager / price
		fee = 0.0075 * crypto
		net = crypto - fee
		trade_number = len(crypto_trade_array)
		return net, price, trade_number

	# Grid trading sell function using a specific sell_wager value determined by the trade number
	# inputs are price, sell_wager determined buy price and situation, buy_wager to calculate a profit and trade number
	# to determine the sell_wager above
	# outputs are net usd recovered, price of the trade and profit from buy to sell
	def sell_grid(price, sell_wager, buy_wager, trade_number):
		trade_value = sell_wager[trade_number]*(.99925)
		usdt = trade_value * price
		fee = 0.0075 * usdt
		net = usdt - fee
		starting_usdt_value = buy_wager[trade_number]
		profit = net - starting_usdt_value
		return net, price, profit


	# START OF BOT #

	# data frames are established and pulled from the data.py file. One is made for each time frame to be analyzed
	# One set for each crypto analyzed
	df_BTC_1m = data.data_BTC_1m().reset_index()
	df_BTC_1d = data.data_BTC_1d().reset_index()
	df_BTC_12h = data.data_BTC_12h().reset_index()
	df_BTC_15m = data.data_BTC_15m().reset_index()
	
	# most often only one set will be analyzed using a singular script, or function, unless the coin has a down coin assosiated to it
	df_BTCDWN_1m = data.data_BTCDWN_1m().reset_index()
	df_BTCDWN_1d = data.data_BTCDWN_1d().reset_index()
	df_BTCDWN_12h = data.data_BTCDWN_12h().reset_index()
	df_BTCDWN_15m = data.data_BTCDWN_15m().reset_index()


# Global variables for rising roof and grid trading strategies
	# Global variables allow for variability in actions based ot the "class" each action is defined by. e.g. if its bull or bear or if the trade requires a pause or not
	global global_rising
	global global_grid

# Class initiations and initial state definitions
	# position class defines active trades, trade states, strategies, and actions -- see position.py file for examples of each
	position = p.Position("OUT")
	# position.long_term_strat()
	position.market_change_bull()
	# Ensures that the for loop will be initiated. otherwise it is bypassed to save memory until pauses are over
	position.ready()
	# global classes for rising roof and grid trading. Class defines trade hierarchy and roof and floor values
	# These are currently not being implimented. It took me so long to figure out how to do the two crypto system I
	# didn't have the time to try to make it more efficient
	global_rising = glv.Global_Rising_Roof("OUT")
	global_grid = glv.Global_Grid("BLANK","BLANK")

# Bank of variables, constants and arrays
# If this can be made into its own file and referenced or cleaned up to be more interperatable that would be ideal. I (Pat) can clean it up if thats the best option
# these variables and arrays are not inputs to the bot, they are never changed manually. The variables and arrays here are counters, place holder arrays and balances

	# General variables and arrays
	buy_price = 1;
	start_date = df_BTC_1m["timestamp"].iloc[0]; 
	end_date = df_BTC_1m["timestamp"].iloc[len(df_BTC_1m)-1];
	timestamp=[];
	wins = 0;
	losses = 0;
	counter= 0;
	market_change_bull = [];
	market_change_bear = [];
	bull_change_times = [];
	bear_change_times = [];
	sell_price = 1;
	Short_action_diff = 0;
	buy_sell_difference = 0;
	buy_sell_derivative = 0;
	bear_market_diff = 0;
	trade_number = 0;
	trade_level = -1;
	level = -1;
	usdt=[];
	sells_short = [];
	sell_times_market = []; 
	sells_market = [];
	buys_short = [];
	
	# BTC general variables and arrays
	BTC_balance = 0;
	BTC=[];
	buy_times_short = [];
	buys_market = [];
	btc_sell_times_w = [];
	buy_times_market = [];
	btc_trade_array = [];
	btc_sells_w = [];
	btc_sell_times_l = [];
	btc_sells_l = [];
	BTC_profit = 0;
	
	# BTC grid variables and arrays
	btc_buy_times_grid = [];  
	btc_buys_grid = [];   
	btc_buy_net = [];
	btc_sells_even = []; 
	btc_sell_times_even = []; 
	btc_sells_grid = []; 
	btc_sells_all = []; 
	btc_sell_times_all = [];
	btc_trade_level_array = [];
	BTC_wager_array = [];
	BTC_sell_wager_array = [];
	btc_max_level_value = 0; 
	btc_min_level_value = 0;
	btc_opened_closed_array = [];
	btc_sells_all=[]; 
	btc_sell_times_all=[];
	btc_sells_grid=[];
	btc_sell_times_grid=[];
	btc_level_array = [];
	
	# BTCDOWN general variables and arrays
	BTCDWN=[]; 
	btcdwn_trade_array = [];
	BTCDWN_wager_array = [];
	BTCDWN_sell_wager_array = [];
	BTCDWN_balance = 0;
	BTCDWN_profit = 0;
	btcdwn_sells_all=[];
	btcdwn_sell_times_all=[];
	btcdwn_sells_grid=[];
	btcdwn_sell_times_grid=[];
	btcdwn_sells_l=[];
	btcdwn_sell_times_l=[];
	btcdwn_sells_w=[];
	btcdwn_sell_times_w=[];
	btc_trade_value_array = [];
	btc_level_value = [];
	
	# BTCDOWN grid variables and arrays
	btcdwn_buys_grid=[];
	btcdwn_buy_times_grid=[];
	btcdwn_sells_even=[];
	btcdwn_sell_times_even=[];
	btcdwn_trade_level_array = [];
	btcdwn_buy_net=[];
	btcdwn_trade_value_array = [];
	btcdwn_level_array = [];
	btcdwn_level_value =[];
	btcdwn_opened_closed_array = [];
	btcdwn_max_level_value = 0;
	btcdwn_min_level_value = 0;
	
	# General grid variables and arrays
	crypto_opened_closed_array = [];
	crypto_balance_array = [];
	crypto_level_value = [];
	crypto_level_array = [];
	crypto_buy_net = [];
	sells_grid = [];
	next_floor = 0;
	next_roof = 0;
	last_roof = 0;
	buy_sell_price = 0;
	min_level_number = 0;
	max_level_number = 0;
	out_even = 0;
	opened_grid_trades = 0;
	closed_grid_trades = 0;
	closed_array = [];
	sell_net = [];
	first_trade = 0;
	closed_trades_array = [];
	closed_where_array = [];
	max_level_counter = 0;
	trade_level_array = [];
	first_trade_number = 0;
	buys_dwn = [] ;
	buy_times_dwn =[];
	sells_dwn = [];
	sell_times_dwn = [];
	trade_profit = 0;
	

	shutil.rmtree('logs')
	os.mkdir("logs")


# INDEX variables to keep applicable data lined up
# Each different index applies to a seperate tracker that counts during the for loop
# This section does not necessarily have to be kept in the live bot since lines in a matrix are not what determines the information read, the last pull from binance does
	index_15m = 0
	index_1d = 0
	index_yesterday = -1
	index_12h = 0
	index_bb = 1
	counter = 0
	cryp_counter = 0
	index_macd = 1
	sell_counter = 0
	above_zero_counter = 0
	midnight = '00:10:00'
	noon = '12:00:00'
	first_day   = 1450
	opened = 0
	closed = 1

# Trading input parameters:

# General Account Inputs:
	# Principle ammount 
	principle = 8000
	# Initial balance
	USDT_balance = 8000

# Grid trading inputs:
# Whether or not the bot is trading BTC or BTCDOWN determines how it trades:
# BTCDOWN is leveraged roughly 3x BTC so when trading with the short coin, grid distances are 3x that of BTC
# Buy in values (percentage of balance into certain trades) can be changed for each as well if that is desired and found more effective
	if global_grid.trade_style == "BULL GRID":
# this section re-defines the generic "crypto data frame" into the first itteration IF manually decided upon by us.
# Otherwise coin selection will be determined on lines (184-204) by RSI parameter classification
		df_crypto_1m = df_BTC_1m
		df_crypto_1d = df_BTC_1d
		df_crypto_15m = df_BTC_15m
		Grid_size = .0125 * df_crypto_1m.iloc[cryp_counter]["close"]
		buy_wager = 0.05 * USDT_balance
		first_wager = buy_wager
	elif global_grid.trade_style == "BEAR GRID":
		df_crypto_1m = df_BTCDWN_1m
		df_crypto_15m = df_BTCDWN_15m
		df_crypto_1d = df_BTCDWN_1d
		Grid_size = .0375 * df_crypto_1m.iloc[cryp_counter]["close"]
		buy_wager = 0.05 * USDT_balance
		first_wager = buy_wager

		
# Rising Roof inputs:
# this can be ignored unless we decide to make a strategy not using BTCDOWN and a VPN and instead use the rising roof strat during the BEAR market
	# rising_roof = 
	# x = [];y = [];index = count()
	
	
# animation function - get working once trading strategy is functional 
# animation is LAST priority. Unless we want to make a simplified one for a presentation
	# def animate(i):

	# x_val = next(index)
	# x.append(x_val)
	# y.append(int(df.iloc[x_val]["close"]))


# Start of action loop of Bot
# the for loops foundation (index variable) is the 1 minute BTC data frame, it can switch back and forth between BTC and BTCDOWN, but doesn't need to
	# for each row in the btc 1m data set. This would not be in the live bot, the actions would be caused by independant functions that would have the 
	# ability to initiate every 10 seconds using the most recent pull of data from the binance servers - see binance_functions.py to determine how seconds 
	# data, that would be requested "manually" by the bot making a query to the binance servers, would be combined with the 1m, 15m, 12h, data that is provided by binance
	for index, row in df_BTC_1m.iterrows():
		
		# counts each row for grid trading actions, does not reset
		cryp_counter += 1
		
		try:
			# general counter used for the 15m time frame to count index_15m every 15 lines
			counter= counter + 1
			
			# if the macd_sig data point is blank, it is too early to run accurate calculations and actions in the short time frame
			if row["MACD_sig"] != np.nan and row["index"] > (first_day)  :
				
				# increases the counter values by one, each time the date parser reads 12:01 am. each night
				# Use this for all 1-day and 12-hour calculations or actions
				if datetime.strftime(date_parser.parse(row["timestamp"]), "%H:%M:%S") == midnight:
					
					index_1d += 1
					index_macd += 1
					index_yesterday += 1
					index_12h += 1
					sell_counter += 1
					index_bb += 1
					
				# increases the counter values by one, each time the date parser reads 12:00 pm. each day
				# Use this ONLY for all 12-hour calculations or actions
				if datetime.strftime(date_parser.parse(row["timestamp"]), "%H:%M:%S") == noon:
					index_12h += 1
					index_bb += 1
					
				# this line is to try to make sure the bot doesn't start making buy or sell orders before the proper metrics have been calculated
				# This WOULD NOT be neccessary for the live bot since the data up to 70 days back already exists (which is the length of longest calculation
				# we have in the script - 70 moving average) so all we need to do is calculate using 70 days prior data and then feed it into the live data
				if position.strategy == "GRID TRADE" and df_BTC_1d.iloc[index_1d]["1dRSI"] != np.nan and index_1d > 30:
					
					# this line means that the grid market (BEAR or BULL) hasn't been manually determined so the bot assigns it, itself
					if global_grid.trade == "BLANK" and global_grid.trade_style == "BLANK" :
						
						# if the 1d rsi for the last two CLOSES are less than 55 than it is too late to catch the short spike in BTCDOWNs price
						# due to the initial dump. Better to slowly hedge your way down and grid trade as BTCs price drops and raises (in the low time frames)
						# and move into the bull market to come
						if df_BTC_1d.iloc[index_1d]["1dRSI"] < 55 and df_BTC_1d.iloc[index_yesterday]["1dRSI"] < 55 :
							
							global_grid.trade_bull()
						# As long as the data frames are defined here, all of the variables that switch back and forth can be calculated foving forward
							df_crypto_1m = df_BTC_1m
							df_crypto_1d = df_BTC_1d
							df_crypto_12h = df_BTC_12h
							df_crypto_15m = df_BTC_15m
							Grid_size = .0125 * df_crypto_1m.iloc[cryp_counter]["close"]
							buy_wager = 0.05 * USDT_balance
							first_wager = buy_wager
							sell_wager = buy_wager/df_crypto_1m.iloc[cryp_counter]["close"]
						
						# see lines 336-338 on explaination of rsi definition
						elif df_BTC_1d.iloc[index_1d]["1dRSI"] > 55 and df_BTC_1d.iloc[index_yesterday]["1dRSI"] > 55 :
							global_grid.trade_bear()
							df_crypto_1m = df_BTCDWN_1m
							df_crypto_15m = df_BTCDWN_15m
							df_crypto_12h = df_BTCDWN_12h
							df_crypto_1d = df_BTCDWN_1d
							Grid_size = .0375 * df_crypto_1m.iloc[cryp_counter]["close"]
							buy_wager = 0.05 * USDT_balance
							first_wager = buy_wager
							sell_wager = buy_wager/df_crypto_1m.iloc[cryp_counter]["close"]
							
					# this part was included to make it so there was a delay after each "blow out" trade, which when the price hits 3.5 bollinger bands so 
					# it automatically sells the whole balance and buys back in at the open of the next day. That or at noon that same day, depending on how aggressive your sells are
					if global_grid.trade == "NOT READY":
						# buys back in the determined balance at noon the next day since the trend is still going in the same direction, we just want to capitalize 
						# on the blow out (only happens once or twice a month on big, quick runs)
						if datetime.strftime(date_parser.parse(df_crypto_1m.iloc[cryp_counter]["timestamp"]), "%H:%M:%S") == noon and global_grid.all_trades_closed == "TRUE":
							global_grid.ready()
						
						
						# If delays are to be implemented use a variation of this.
						# primarily used for the grid or long term traiding of a single crypto, when coins and their short counterparts are 
						# paired, a delay is not necessary and performs worse when used
						
						# print('ready for delay')
						# if df_BTC_1d.iloc[index_1d]["1dRSI"] < 15 and position.state == "OUT" :
						# 	position.state = "IN"
						# elif position.state == "IN" and df_BTC_1d.iloc[index_1d]["1dRSI"] > 25 :
						# 	global_grid.ready()
						# 	print('ready')
						# 	print("########################GRID DELAY OFF(market dump)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# 	print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# 	print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						
						# if df_BTC_1d.iloc[index_1d]["1dRSI"] > 65 and position.state == "OUT" and global_grid.all_trades_closed == "TRUE" :
						# 	global_grid.ready()
						# 	print("########################GRID DELAY ON(market correction)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# 	print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# 	print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# 	print(f'RSI:{df_BTC_1d.iloc[index_1d]["1dRSI"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# elif position.state == "OUT" and df_BTC_1d.iloc[index_1d]["1dRSI"] < 65 and global_grid.all_trades_closed == "TRUE" :
						# 	# global_grid.switch_trends()
						# 	global_grid.ready()
						# 	print('ready')
						# 	print("########################GRID DELAY OFF(market correction)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# 	print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# 	print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						# 	print(f'RSI:{df_BTC_1d.iloc[index_1d]["1dRSI"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
						 # and df_crypto_1d.iloc[index_12h]['close'] <  df_crypto_1d.iloc[index_12h]['Upper_band']
						
						
						
					
				
				# A "print_to_file.py" would be ideal for all of these print clusters(a rough initial attempt is in the bot.py folder)
				# They take up a lot of space here but they are pretty variable to there would have to be a lot of 
				# itterations in the seperate file as well and just called for in this script as a function
				
							print("########################GRID DELAY ON(market correction)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f'RSI:{df_BTC_1d.iloc[index_1d]["1dRSI"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							
					# Start of grid trading logic. If NOT READY then only sale orders can be filled. Buys are restricted
					if global_grid.trade == "READY"	:
						
						# this logic determines if it is the first trade or not. The first trade has different parameters, namely the size of the buy
						# the first trade also is not re sold for grid profit during the process and is sold only at the end of the series, the "sell all"
						if global_grid.made_first_trade == "FALSE" and USDT_balance > first_wager and global_grid.all_trades_closed == "TRUE" :
							
							# if bull grid is defined in the initial conditions at the beginning or the 
							if global_grid.trade_style == "BULL GRID" and global_grid.made_first_trade == "FALSE" :
								
						# if grid trading strat is determined as BULL (general trend is either going up or going down but determined that would soon be going up)	
								crypto = str('BTC')
								crypto_sell_wager_array = BTC_sell_wager_array
								crypto_wager_array = BTC_wager_array
								crypto_wager = buy_wager
								crypto_sell_wager = sell_wager
								crypto_balance = BTC_balance
								crypto_profit = BTC_profit
								crypto_sell_times_grid = btc_sell_times_grid
								crypto_sell_times_all = btc_sell_times_all
								crypto_sell_times_even = btc_sell_times_even
								crypto_buys_grid = btc_buys_grid
								crypto_buy_times_grid = btc_buy_times_grid
								crypto_sells_even = btc_sells_even
								crypto_sell_times_w = btc_sell_times_w
								crypto_sells_w = btc_sells_w
								crypto_sells_all = btc_sells_all
								crypto_balance_array = BTC
								crypto_trade_level_array = btc_trade_level_array
								crypto_level_array = btc_level_array
								crypto_buy_net = btc_buy_net
								crypto_trade_value_array = btc_trade_value_array
								crypto_level_value = btc_level_value
								crypto_opened_closed_array = btc_opened_closed_array
								crypto_trade_array = btc_trade_array
								crypto_min_level_value = btc_min_level_value
								crypto_max_level_value = btc_max_level_value
								df_crypto_1d = df_BTC_1d
								df_crypto_1m = df_BTC_1m
								df_crypto_15m = df_BTC_15m
								df_crypto_12h = df_BTC_12h
								print('crypto chosen')
								print(crypto)
								position.state = "IN"									
							
							elif global_grid.trade_style == "BEAR GRID" and global_grid.made_first_trade == "FALSE" :
								
						# if BEAR is chosen then the opposite applies as is stated above. The trend is going down or determined to be a peak that would soon crash		
								crypto = str('BTCDWN')
								crypto_sell_wager_array = BTCDWN_sell_wager_array
								crypto_wager_array = BTCDWN_wager_array
								crypto_wager = buy_wager
								crypto_sell_wager = sell_wager
								crypto_balance = BTCDWN_balance
								crypto_profit = BTCDWN_profit
								df_crypto_1d = df_BTCDWN_1d
								df_crypto_1m = df_BTCDWN_1m
								df_crypto_15m = df_BTCDWN_15m
								df_crypto_12h = df_BTCDWN_15m
								crypto_sell_times_grid = btcdwn_sell_times_grid
								crypto_sell_times_all = btcdwn_sell_times_all
								crypto_sell_times_even = btcdwn_sell_times_even
								crypto_buys_grid = btcdwn_buys_grid
								crypto_buy_times_grid = btcdwn_buy_times_grid
								crypto_sells_even = btcdwn_sells_even
								crypto_sells_grid = btcdwn_sells_grid
								crypto_sell_times_w = btcdwn_sell_times_w
								crypto_sells_w = btcdwn_sells_w	
								crypto_sells_all = btcdwn_sells_all 
								crypto_balance_array = BTCDWN 
								crypto_trade_level_array = btcdwn_trade_level_array	
								crypto_level_array = btcdwn_trade_level_array
								crypto_level_value = btcdwn_level_value
								crypto_buy_net = btcdwn_buy_net
								crypto_trade_value_array = btcdwn_trade_value_array	
								crypto_opened_closed_array = btcdwn_opened_closed_array	
								crypto_trade_array = btcdwn_trade_array
								crypto_min_level_value = btcdwn_min_level_value
								crypto_max_level_value = btcdwn_max_level_value					
								print('crypto chosen')
								print(crypto)	
								position.state = "IN"
								
							# applicable to either coin on the first trade. 
							# the first trade determines:
								# the grid height (as a percentage of the current price) 
								# Resets grid trade variables to 0, such as trade number and so on
								# First trade is never sold until the final strategy switch trade i.e from BULL to BEAR
							
							print('buy first')
							print(USDT_balance)
							crypto_wager = .75 * USDT_balance
							crypto_trade_array = 0
							crypto_trade_array = []
							first_trade_number = trade_number
							rtn = buy_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_wager,crypto_trade_array)
							global_grid.made_first_trade = "TRUE"
							crypto_profit = rtn[0]
							buy_price = rtn[1]
							trade_number = 0
							USDT_balance = USDT_balance - crypto_wager
							crypto_balance = crypto_balance + crypto_profit
							trade_level = 0
							level = 0					
							crypto_buy_times_grid.append(df_crypto_1m.iloc[cryp_counter]["index"])
							crypto_buys_grid.append(buy_price)
							crypto_buy_net.append(crypto_profit)
							crypto_balance_array.append(crypto_balance)
							usdt.append(USDT_balance)
							crypto_trade_array.append(trade_number)
							crypto_wager_array.append(crypto_wager)
							crypto_sell_wager_array.append(crypto_sell_wager)
	# Each level will be based on this initial trade. this and, wager and grid size can be changed down the road 
							crypto_level_array.append(level)
							crypto_trade_level_array.append(trade_level)
							crypto_trade_value_array.append(df_crypto_1m.iloc[cryp_counter]['close'])
							crypto_level_value.append(df_crypto_1m.iloc[cryp_counter]['close'])
							crypto_min_level_value = crypto_level_value[-1]
							crypto_max_level_value = crypto_level_value[-1]
							crypto_opened_closed_array.append(opened)
							opened_grid_trades += 1
							position.state = "IN"
							above_zero_counter=0
							buy_down_counter=0
							buy_up_counter=0
							buy_sell_price = df_crypto_1m.iloc[cryp_counter]['close']
							first_wager = crypto_wager
							first_profit = crypto_profit
							if len(crypto_buys_grid) == 1:
								first_trade = 1
								frist_trade = crypto_buys_grid[-1]
								first_trade_value = principle/first_trade
								market_value = first_trade_value * df_crypto_1m.iloc[cryp_counter]["close"]								
							print("#########################BUY-FIRST TRADE#############################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))							
							print(f"BUY-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f'BTC_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f'BTCDWN_Price:{df_BTCDWN_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))							
							print(f"MARKET VALUE:{market_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"WAGER:{crypto_wager_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"TRADE NUMBER:{crypto_trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
							print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))																			
							print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							if global_grid.trade_style == "BULL GRID":
								Grid_size = .0125 * df_crypto_1m.iloc[cryp_counter]["close"] 
							elif global_grid.trade_style == "BEAR GRID":
								Grid_size = .0375 * df_crypto_1m.iloc[cryp_counter]["close"]
							next_floor = crypto_level_value[-1] - Grid_size
							next_roof = crypto_level_value[-1] + Grid_size
							last_roof = crypto_level_value[-1]						

						if df_crypto_1d.iloc[index_1d]["1dRSI"] > 65 and df_crypto_1d.iloc[index_yesterday]["1dRSI"] > 65 and global_grid.wait_to_sell == "FALSE" and global_grid.trade_style == "BULL GRID" :
							global_grid.wait_to_sell = "TRUE" 
							print("#########################WAIT TO SELL###############################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"TIME-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f'LEVEL NUMBER:{level - 1}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f'PRICE:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))

						if df_crypto_1d.iloc[index_1d]["1dRSI"] > 59 and global_grid.trade_style == "BEAR GRID" and global_grid.wait_to_sell == "FALSE" :
							global_grid.wait_to_sell = "TRUE" 
							print("#########################WAIT TO SELL###############################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"TIME-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f'LEVEL NUMBER:{level - 1}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							print(f'PRICE:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))




						if df_crypto_1m.iloc[cryp_counter]["close"] < next_floor and global_grid.made_first_trade == "TRUE" :
							market_value = first_trade_value * df_crypto_1m.iloc[cryp_counter]["close"]	
							crypto_level_value.append(next_floor)							
							next_floor = crypto_level_value[-1] - Grid_size
							next_roof = crypto_level_value[-1] + Grid_size
							last_roof = crypto_level_value[-1]
							max_level_counter = 0
							level -= 1
							crypto_level_array.append(level)
							buy_up_counter = 0
							buy_down_counter += 1
							above_zero_counter -= 1
							global_grid.all_trades_closed = "FALSE"
							if df_crypto_1m.iloc[cryp_counter]["close"] < next_floor:
								crypto_level_value.append(next_roof)							
								add_levels = math.floor((df_crypto_1m.iloc[cryp_counter]["close"]- next_floor)/Grid_size)
								next_roof = crypto_level_value[-1] - add_levels * Grid_size
								# last_roof = crypto_level_value[-1]
								level += add_levels
								crypto_level_array.append(level)
								buy_up_counter += 1
								above_zero_counter += add_levels

							if crypto_level_value[-1] < crypto_min_level_value :
								crypto_min_level_value = min(crypto_level_value)
								print("#########################LEVEL ADDED###############################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"TIME-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f'LEVEL NUMBER:{level - 1}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"LEVEL-{next_floor}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f'PRICE:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
							
							if USDT_balance <= 0 :
								global_grid.out_of_money()								

							if USDT_balance > 0 :
								crypto_wager = (0.05 + above_zero_counter * 0.05) * USDT_balance	
								if crypto_wager < 500 :
									crypto_wager = 500
								if USDT_balance < crypto_wager:
									crypto_wager = USDT_balance
								print('buy down')
								rtn = buy_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_wager,crypto_trade_array)
								crypto_profit = rtn[0]
								buy_price = rtn[1]
								trade_number = rtn[2]
								USDT_balance = USDT_balance - crypto_wager
								crypto_balance = crypto_balance + crypto_profit		
								crypto_buy_times_grid.append(df_crypto_1m.iloc[cryp_counter]["index"])
								crypto_buys_grid.append(buy_price)
								crypto_buy_net.append(crypto_profit)
								crypto_balance_array.append(crypto_balance)
								usdt.append(USDT_balance)
								crypto_trade_array.append(trade_number)
								crypto_wager_array.append(crypto_wager)
								crypto_sell_wager_array.append(crypto_sell_wager)			
								crypto_opened_closed_array.append(opened)
								opened_grid_trades += 1
								trade_level -= 1
								crypto_trade_level_array.append(trade_level)
								crypto_trade_value_array.append(last_roof)	
								global_grid.balance = "FULL"							
								print("#########################BUY-GRID-DOWN##########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))									
								print(f"BUY-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f'BUY_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"MARKET VALUE:{market_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"WAGER:{crypto_wager_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"TRADE NUMBER:{crypto_trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
								print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))													
								print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								buy_sell_price = df_crypto_1m.iloc[cryp_counter]["close"]		

						elif df_crypto_1m.iloc[cryp_counter]["close"] > next_roof and global_grid.made_first_trade == "TRUE" :
							market_value = first_trade_value * df_crypto_1m.iloc[cryp_counter]["close"]	
							crypto_level_value.append(next_roof)							
							next_floor = crypto_level_value[-1] - Grid_size
							next_roof = crypto_level_value[-1] + Grid_size
							last_roof = crypto_level_value[-1]
							level += 1
							crypto_level_array.append(level)
							buy_down_counter = 0
							buy_up_counter += 1
							above_zero_counter += 1
							if df_crypto_1m.iloc[cryp_counter]["close"] > next_roof:
								crypto_level_value.append(next_roof)							
								add_levels = math.floor((df_crypto_1m.iloc[cryp_counter]["close"]- next_roof)/Grid_size)
								next_roof = crypto_level_value[-1] + add_levels * Grid_size
								# last_roof = crypto_level_value[-1]
								level += add_levels
								crypto_level_array.append(level)
								buy_up_counter += 1
								above_zero_counter += add_levels

							if crypto_level_value[-1] > crypto_max_level_value :
								crypto_max_level_value = max(crypto_level_value)
								max_level_counter += 1

								if max_level_counter >= 1 :
									global_grid.all_trades_closed = "TRUE"						
								print("#########################LEVEL ADDED#################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"TIME-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f'LEVEL NUMBER:{level + 1}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"LEVEL-{next_roof}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f'PRICE:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))

							if USDT_balance <= 0 :
								global_grid.out_of_money()
							
							elif USDT_balance > 0:
								crypto_wager = 0.2 * USDT_balance + above_zero_counter * .025 * USDT_balance + above_zero_counter * .05 * USDT_balance
								if crypto_wager < 500 :
									crypto_wager = 500
								if USDT_balance < crypto_wager:
									crypto_wager = USDT_balance								 	
								rtn = buy_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_wager,crypto_trade_array)
								print('buy up')
								crypto_profit = rtn[0]
								buy_price = rtn[1]
								trade_number = rtn[2]
								USDT_balance = USDT_balance - crypto_wager
								crypto_balance = crypto_balance + crypto_profit														
								crypto_buy_times_grid.append(df_crypto_1m.iloc[cryp_counter]["index"])
								crypto_buys_grid.append(buy_price)
								crypto_buy_net.append(crypto_profit)
								crypto_balance_array.append(crypto_balance)
								usdt.append(USDT_balance)							
								crypto_trade_array.append(trade_number)
								crypto_wager_array.append(crypto_wager)
								crypto_sell_wager_array.append(crypto_sell_wager)		
								crypto_opened_closed_array.append(opened)
								opened_grid_trades += 1
								trade_level += 1
								crypto_trade_level_array.append(trade_level)
								crypto_trade_value_array.append(last_roof)
								global_grid.balance = "FULL"
								print("#########################BUY-GRID-UP###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))									
								print(f"BUY-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f'BUY_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"WAGER:{crypto_wager_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"TRADE NUMBER:{crypto_trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
								print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))												
								print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								buy_sell_price = df_crypto_1m.iloc[cryp_counter]["close"]
# and len(np.where(np.array(crypto_trade_level_array) == last_roof)[-1]) > 1
							if crypto_balance > first_profit and buy_up_counter >= 2 :
								# sell action for the last buy, one grid level below, taking profit and buying again 								
								if global_grid.all_trades_closed == "FALSE" and df_crypto_1m.iloc[cryp_counter]["close"] > last_roof :
									# print("try to sell")
									if global_grid.balance == "FULL":
										trade_level_value_array = np.array([crypto_trade_level_array])
										trades_equal_to = np.where(trade_level_value_array == (trade_level - 1))
										trade_number_open_array_full = np.array(trades_equal_to[-1])
										# print(trade_number_open_array)
										trade_number_open = trade_number_open_array_full[(len((trade_number_open_array_full)) - 2)]
										# print(trade_number_open)		
										# if len(trade_number_open) > 2:
										# 	trade_number_open_array = trade_number_open
										# 	trade_number_open = np.array(trade_number_open_array)[-1]
									elif global_grid.balance == "EMPTY":
										level_value_array = np.array([crypto_level_value])
										trades_equal_to = np.where(level_value_array == (next_roof - 2*Grid_size))
										trade_value_array_empty = np.array(trades_equal_to[0])
										# print(trade_number_open_array)
										trade_number_open_empty = trade_value_array_empty[(len(np.array(trade_value_array_empty)) - 2)]
										trade_number_open_where_array = np.where(crypto_trade_level_array == trade_number_open_empty)
										trade_number_open_array = trade_number_open_where_array[-1]
										trade_number_open = trade_number_open_array[-1]
									# 	print(trade_number_open)
										print('out of money')		
										# if len(trade_number_open) > 2:
										# 	trade_number_open_array = trade_number_open
										# 	trade_number_open = np.array(trade_number_open_array)[-1]

									if trade_number_open == first_trade_number :
										print("#########################PASS FIRST TRADE#################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TIME-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'LEVEL NUMBER:{first_trade_number}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"LEVEL-{next_roof}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'PRICE:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										
									elif crypto_opened_closed_array[trade_number_open] == opened :	
										print('sell even')
										sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_buy_net, crypto_wager_array, trade_number_open)
										out_even += 1
										closed_grid_trades += 1										
										closed_np_array = np.array(crypto_opened_closed_array)
										crypto_opened_closed_array.pop(trade_number_open)
										crypto_opened_closed_array.insert(trade_number_open, closed)
										USDT_profitORloss = sell_action[0]
										sell_price = sell_action[1]
										trade_profit = sell_action[2]
										crypto_balance = crypto_balance - crypto_buy_net[trade_number_open]
										USDT_balance = USDT_balance + USDT_profitORloss
										USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
										crypto_sell_times_even.append(df_crypto_1m.iloc[cryp_counter]["index"])
										crypto_sells_even.append(df_crypto_1m.iloc[cryp_counter]["close"])
										sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
										crypto_balance_array.append(crypto_balance)
										usdt.append(USDT_balance)
										timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])					
										print("######################SELL-EVEN-BUY AND SELL(even - 1)#####################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
										print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"WAGER:{crypto_buy_net[trade_number_open]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"EVEN TRADES:{out_even}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))							
										print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE NUMBER:{trade_number_open}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
										print(f"LEVEL:{crypto_level_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
										print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										
									if crypto_opened_closed_array[trade_number - 2] == opened :	
										sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_buy_net, crypto_wager_array, (trade_number-2))									
										wins += 1
										closed_grid_trades += 1										
										closed_np_array = np.array(crypto_opened_closed_array)
										crypto_opened_closed_array.pop(trade_number - 2)
										crypto_opened_closed_array.insert(trade_number - 2, closed)									
										USDT_profit = sell_action[0]
										sell_price = sell_action[1]
										trade_profit = sell_action[2]
										crypto_balance = crypto_balance - crypto_buy_net[trade_number - 2]
										USDT_balance = USDT_balance + USDT_profit
										USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
										crypto_sell_times_w.append(df_crypto_1m.iloc[cryp_counter]["index"])
										crypto_sells_w.append(df_crypto_1m.iloc[cryp_counter]["close"])
										sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
										crypto_balance_array.append(crypto_balance)
										usdt.append(USDT_balance)
										timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])			
										print("#######################SELL-WIN-BUY AND SELL(-2)#######################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))											
										print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"WAGER:{crypto_buy_net[trade_number - 2]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE NUMBER:{crypto_trade_array[trade_number - 2]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
										print(f"LEVEL:{crypto_level_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
										print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										if len(trade_number_open_array_full) > 2 and crypto_opened_closed_array[trade_number_open - 1] == opened  :
											print('sell double')
											trade_number_open_dub = trade_number_open_array_full[len(trade_number_open_array) - 3]
											if trade_number_open_dub == opened :
												sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_buy_net, crypto_wager_array, trade_number_open_dub)
												out_even += 1
												closed_grid_trades += 1										
												closed_np_array = np.array(crypto_opened_closed_array)
												crypto_opened_closed_array.pop(trade_number_open_dub)
												crypto_opened_closed_array.insert(trade_number_open_dub, closed)
												USDT_profitORloss = sell_action[0]
												sell_price = sell_action[1]
												trade_profit = sell_action[2]
												crypto_balance = crypto_balance - crypto_buy_net[trade_number_open_dub]
												USDT_balance = USDT_balance + USDT_profitORloss
												USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
												crypto_sell_times_even.append(df_crypto_1m.iloc[cryp_counter]["index"])
												crypto_sells_even.append(df_crypto_1m.iloc[cryp_counter]["close"])
												sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
												crypto_balance_array.append(crypto_balance)
												usdt.append(USDT_balance)
												timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])					
												print("######################SELL-EVEN-BUY AND SELL(even - double)#####################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
												print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
												print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
												print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
												print(f"WAGER:{crypto_buy_net[trade_number_open_dub]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
												print(f"EVEN TRADES:{out_even}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))							
												print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
												print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
												print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
												print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
												print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
												print(f"TRADE NUMBER:{trade_number_open_dub}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
												print(f"LEVEL:{crypto_level_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
												print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
												print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											
											sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_buy_net, crypto_wager_array, (trade_number_open - 1))									
											wins += 1
											closed_grid_trades += 1										
											closed_np_array = np.array(crypto_opened_closed_array)
											crypto_opened_closed_array.pop(trade_number_open - 1)
											crypto_opened_closed_array.insert(trade_number_open - 1, closed)									
											USDT_profit = sell_action[0]
											sell_price = sell_action[1]
											trade_profit = sell_action[2]
											crypto_balance = crypto_balance - crypto_buy_net[trade_number_open - 1]
											USDT_balance = USDT_balance + USDT_profit
											USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
											crypto_sell_times_w.append(df_crypto_1m.iloc[cryp_counter]["index"])
											crypto_sells_w.append(df_crypto_1m.iloc[cryp_counter]["close"])
											sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
											crypto_balance_array.append(crypto_balance)
											usdt.append(USDT_balance)
											timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])			
											print("#######################SELL-WIN-BUY AND SELL(-2 - double)#######################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))												
											print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											print(f"WAGER:{crypto_buy_net[trade_number_open - 1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
											print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
											print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											print(f"TRADE NUMBER:{crypto_trade_array[trade_number_open - 1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
											print(f"LEVEL:{crypto_level_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
											print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
											print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))

								elif crypto_opened_closed_array[trade_number-2] == opened :
									if (trade_number - 2) == first_trade_number :
										print("#########################PASS FIRST TRADE#################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TIME-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'LEVEL NUMBER:{first_trade_number}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"LEVEL-{next_roof}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'PRICE:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										pass 
									else:
										print("sell only")
										sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_buy_net, crypto_wager_array, (trade_number-2))
										wins += 1
										closed_grid_trades += 1										
										closed_np_array = np.array(crypto_opened_closed_array)
										crypto_opened_closed_array.pop(trade_number - 2)
										crypto_opened_closed_array.insert(trade_number - 2, closed)
										USDT_profit = sell_action[0]
										sell_price = sell_action[1]
										trade_profit = sell_action[2]
										crypto_balance = crypto_balance - crypto_buy_net[trade_number - 2]
										USDT_balance = USDT_balance + USDT_profit
										USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
										crypto_sell_times_w.append(df_crypto_1m.iloc[cryp_counter]["index"])
										crypto_sells_w.append(df_crypto_1m.iloc[cryp_counter]["close"])
										sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
										crypto_balance_array.append(crypto_balance)
										usdt.append(USDT_balance)
										timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])									
										print("########################SELL-WIN-BUY AND SELL(-2)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"WAGER:{crypto_buy_net[trade_number-2]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE NUMBER:{crypto_trade_array[trade_number - 2]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
										print(f"LEVEL:{crypto_level_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
										print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# if above_zero_counter == 5:
									# 	wins += 1
									# 	sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_buy_net, crypto_wager_array, (trade_number-1))
									# 	USDT_profit = sell_action[0]
									# 	sell_price = sell_action[1]
									# 	trade_profit = sell_action[2]
									# 	crypto_balance = crypto_balance - crypto_buy_net[trade_number - 1]
									# 	USDT_balance = USDT_balance + USDT_profit
									# 	USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
									# 	sell_times_w.append(df_crypto_1m.iloc[cryp_counter]["index"])
									# 	sells_w.append(df_crypto_1m.iloc[cryp_counter]["close"])
									# 	sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
									# 	BTC.append(crypto_balance)
									# 	usdt.append(USDT_balance)
									# 	next_floor = crypto_level_value[-1] - Grid_size
									# 	next_roof = crypto_level_value[-1] + Grid_size
									# 	last_roof = crypto_level_value[-1]	
									# 	timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])
									# 	# closed_array = np.array(closed_array)
									# 	# closed_array[-1] = np.where(closed_array[trade_number-1] == 0, 1)		
									# 	# closed_array.append(closed_array)
									# 	closed_grid_trades += 1										
									# 	print("######################SELL-WIN-BUY AND SELL(-1)########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# 	print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# 	print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# 	print(f"WAGER:{crypto_buy_net[trade_number-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
									# 	print(f"BTC_Balance:{BTC_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# 	print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# 	print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# 	print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
									# 	print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# 	print(f"TRADE NUMBER:{crypto_trade_array[trade_number - 1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
									# 	print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# 	print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
									# 	print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										
									if crypto_level_value[-1] > crypto_max_level_value:
										crypto_max_level_value = max(crypto_level_value)
										global_grid.all_trades_closed = "TRUE"						
										print("#########################LEVEL ADDED################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TIME-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'LEVEL NUMBER:{trade_level}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"LEVEL-{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'PRICE:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))


								# and crypto_level_value[-1] > max(crypto_level_value[np.array((crypto_opened_closed_array) == 0)[-1]]) and last_roof > crypto_level_value[trade_number - 2]
								if len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]) > 4 and df_crypto_1m.iloc[cryp_counter]["close"] >= crypto_max_level_value :
									# print("went up - sell all")
									crypto_wager_array.pop(trade_number -2)
									if USDT_balance == USDT_profit :
										crypto_wager_array.insert(trade_number - 2, crypto_balance - crypto_buy_net[first_trade_number])
										crypto_profit = 0									
									else:
										crypto_wager_array.insert(trade_number - 2, (crypto_balance - crypto_profit - crypto_buy_net[first_trade_number]))
									# print(crypto_wager_array[trade_number - 2])
									sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_wager_array, crypto_wager_array, (trade_number-2))
									wins += len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]) - 1
									closed_grid_trades += (len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]) - 1)								
									for x in np.where(np.array(crypto_opened_closed_array) == 0)[-1] :
										closed_np_array = np.array(crypto_opened_closed_array)
										crypto_opened_closed_array.pop(x)
										crypto_opened_closed_array.insert(x, closed)
									USDT_profit = sell_action[0]
									sell_price = sell_action[1]
									trade_profit = sell_action[2]
									crypto_balance = crypto_profit + crypto_buy_net[first_trade_number]
									USDT_balance = USDT_balance + USDT_profit
									USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
									crypto_sell_times_all.append(df_crypto_1m.iloc[cryp_counter]["index"])
									crypto_sells_all.append(df_crypto_1m.iloc[cryp_counter]["close"])
									sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
									crypto_balance_array.append(crypto_balance)
									usdt.append(USDT_balance)
									timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])
									# print(USDT_profit)
									# print(crypto_wager_array[trade_number-2])									
									print("########################SELL-WIN-BUY AND SELL(all)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
									print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"WAGER:{crypto_wager_array[trade_number-2]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
									print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
									print(f"RSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"TRADE NUMBER:{crypto_trade_array[np.where(np.array(crypto_opened_closed_array) == 0)[-1]]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
									print(f"LEVEL:{crypto_level_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
									print("############################################################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									# global_grid.made_first_trade == "FALSE"
									# global_grid.all_trades_closed == "TRUE"
									buy_up_counter = 1
									buy_down_counter = 0
							# and df_crypto_1m.iloc[cryp_counter]['close'] > last_roof and len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]) > 2 
							if  crypto_balance_array[-1] > 0 and df_BTC_1m.iloc[cryp_counter]['close'] > .975 * df_crypto_12h.iloc[index_bb]["Upper_band"] and global_grid.trade_style == "BULL GRID" :
								# print('bull intro')
								# print(f"CLOSE:{df_crypto_1m.iloc[cryp_counter]['close']}")
								# print(f"UPPER BAND:{df_crypto_12h.iloc[index_bb]['Upper_band']}")
								# print(index_12h)
								# print(index_1d)
								# print(df_crypto_1m.iloc[cryp_counter]['timestamp'])
								
								if global_grid.trade_style == "BULL GRID":
									df_crypto_12h = df_BTC_12h
								elif global_grid.trade_style == "BEAR GRID":
									df_crypto_12h = df_BTCDWN_12h

								
								print('sell bull')
								sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_balance_array, crypto_wager_array, -1)
								wins += len(np.where(np.array(crypto_opened_closed_array) == 0)[-1])
								closed_grid_trades += (len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]))
								print(closed_grid_trades)								
								for x in np.where(np.array(crypto_opened_closed_array) == 0)[-1] :
									closed_np_array = np.array(crypto_opened_closed_array)
									crypto_opened_closed_array.pop(x)
									crypto_opened_closed_array.insert(x, closed)
								USDT_profit = sell_action[0]
								sell_price = sell_action[1]
								crypto_balance = 0
								USDT_balance = USDT_balance + USDT_profit 
								USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
								crypto_sell_times_all.append(df_crypto_1m.iloc[cryp_counter]["index"])
								crypto_sells_all.append(df_crypto_1m.iloc[cryp_counter]["close"])
								sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
								crypto_balance_array.append(crypto_balance)
								usdt.append(USDT_balance)
								timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])									
								print("########################SELL-WIN-BUY AND SELL(bull run - return)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))									
								print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"WAGER:{crypto_balance_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
								print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"UPPER BAND:{df_crypto_12h.iloc[index_bb]['Upper_band']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"PREV UPPER BAND:{df_crypto_12h.iloc[index_12h]['Upper_band']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))																												
								print(f"1dRSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"TRADE NUMBER:{crypto_trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
								print(f"LEVEL:{crypto_level_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
								buy_sell_price = df_crypto_1m.iloc[cryp_counter]["close"]
								# print(USDT_balance)
								global_grid.wait_to_sell = "FALSE"
								global_grid.all_trades_closed = "TRUE"
								global_grid.not_ready()
								buy_up_counter = 0
								buy_down_counter = 0
							
							elif  crypto_balance_array[-1] > 0 and df_BTCDWN_1m.iloc[cryp_counter]['close'] > 1 * df_crypto_12h.iloc[index_bb]["Upper_band"] and global_grid.trade_style == "BEAR GRID" :
								# print('bull intro')
								# print(f"CLOSE:{df_crypto_1m.iloc[cryp_counter]['close']}")
								# print(f"UPPER BAND:{df_crypto_12h.iloc[index_bb]['Upper_band']}")
								# print(index_12h)
								# print(index_1d)
								# print(df_crypto_1m.iloc[cryp_counter]['timestamp'])
								
								if global_grid.trade_style == "BULL GRID":
									df_crypto_12h = df_BTC_12h
								elif global_grid.trade_style == "BEAR GRID":
									df_crypto_12h = df_BTCDWN_12h

								
								print('sell bull')
								sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_balance_array, crypto_wager_array, -1)
								wins += len(np.where(np.array(crypto_opened_closed_array) == 0)[-1])
								closed_grid_trades += (len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]))
								print(closed_grid_trades)								
								for x in np.where(np.array(crypto_opened_closed_array) == 0)[-1] :
									closed_np_array = np.array(crypto_opened_closed_array)
									crypto_opened_closed_array.pop(x)
									crypto_opened_closed_array.insert(x, closed)
								USDT_profit = sell_action[0]
								sell_price = sell_action[1]
								crypto_balance = 0
								USDT_balance = USDT_balance + USDT_profit 
								USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
								crypto_sell_times_all.append(df_crypto_1m.iloc[cryp_counter]["index"])
								crypto_sells_all.append(df_crypto_1m.iloc[cryp_counter]["close"])
								sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
								crypto_balance_array.append(crypto_balance)
								usdt.append(USDT_balance)
								timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])									
								print("########################SELL-WIN-BUY AND SELL(bull run - return)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))									
								print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"WAGER:{crypto_balance_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
								print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"UPPER BAND:{df_crypto_12h.iloc[index_bb]['Upper_band']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"PREV UPPER BAND:{df_crypto_12h.iloc[index_12h]['Upper_band']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))																												
								print(f"1dRSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"TRADE NUMBER:{crypto_trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
								print(f"LEVEL:{crypto_level_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
								print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
								buy_sell_price = df_crypto_1m.iloc[cryp_counter]["close"]
								# print(USDT_balance)
								global_grid.wait_to_sell = "FALSE"
								global_grid.all_trades_closed = "TRUE"
								global_grid.not_ready()
								buy_up_counter = 0
								buy_down_counter = 0

								# global_grid.made_first_trade = "FALSE"
											

# sell action for the OPEN trade that was bought on the downward slope of the price valley at the SAME LEVEL as we are now on the upward slope
# and crypto_level_value[max(np.where(crypto_level_value == next_roof))] == next_roof and global_grid.all_trades_closed == "FALSE"
	

						if global_grid.made_first_trade == "TRUE" and global_grid.all_trades_closed == "FALSE" and global_grid.trade == "READY" and global_grid.wait_to_sell == "TRUE": 
							# print('try to switch')
							# and df_crypto_1m.iloc[cryp_counter]['close'] > last_roof and len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]) > 2 
							if  position.state == "IN" and df_crypto_1m.iloc[cryp_counter]['close'] > last_roof and global_grid.trade_style == "BULL GRID" :
								# if df_crypto_12h.iloc[index_12h]['STMA_1st_derivative'] > 0:	
								if (df_crypto_1d.iloc[index_1d]["1dRSI"] < 62.5 and df_crypto_1d.iloc[index_1d]["Bol_band_width"] < 1 ) or (df_crypto_1d.iloc[index_1d]["1dRSI"] < 70 and df_crypto_1d.iloc[index_1d]["Bol_band_width"] > 1 ) :
									if df_crypto_1d.iloc[index_1d]["LTMA"] > df_crypto_1d.iloc[index_1d]["STMA"]:
										global_grid.wait_to_sell = "FALSE"
										print('pass')
										pass
									else:
										global_grid.made_first_trade = "FALSE"
										print('sell all bull')
										sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_balance_array, crypto_wager_array, -1)
										wins += len(np.where(np.array(crypto_opened_closed_array) == 0)[-1])
										closed_grid_trades += (len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]))
										print(closed_grid_trades)								
										for x in np.where(np.array(crypto_opened_closed_array) == 0)[-1] :
											closed_np_array = np.array(crypto_opened_closed_array)
											crypto_opened_closed_array.pop(x)
											crypto_opened_closed_array.insert(x, closed)
										USDT_profit = sell_action[0]
										sell_price = sell_action[1]
										crypto_balance = 0
										USDT_balance = USDT_balance + USDT_profit 
										USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
										crypto_sell_times_all.append(df_crypto_1m.iloc[cryp_counter]["index"])
										crypto_sells_all.append(df_crypto_1m.iloc[cryp_counter]["close"])
										sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
										crypto_balance_array.append(crypto_balance)
										usdt.append(USDT_balance)
										timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])									
										print("########################SELL-WIN-BUY AND SELL(switch trends-bull)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))									
										print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"WAGER:{crypto_balance_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"1dRSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE NUMBER:{crypto_trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
										print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
										buy_sell_price = df_crypto_1m.iloc[cryp_counter]["close"]
										print(USDT_balance)
										global_grid.wait_to_sell = "FALSE"
										max_level_value = 0
										min_level_value = 0
										if global_grid.trade_style == "BULL GRID":
											BTC_sell_wager_array = (crypto_sell_wager_array)
											BTC_wager_array = (crypto_wager_array)
											buy_wager = crypto_wager 
											sell_wager = crypto_sell_wager 
											BTC_balance = crypto_balance 
											BTC_profit = crypto_profit 
											df_BTC_1d = df_crypto_1d 
											df_BTC_1m = df_crypto_1m 
											df_BTC_15m = df_crypto_15m
											df_BTC_12h = df_crypto_12h
											btc_sell_times_all = (crypto_sell_times_all)
											btc_sell_times_even = (crypto_sell_times_even)
											btc_buys_grid = (crypto_buys_grid)
											btc_buy_times_grid = (crypto_buy_times_grid)
											btc_sells_even = (crypto_sells_even)
											btc_sells_all = (crypto_sells_all)
											btc_sell_times_w = (crypto_sell_times_w)
											btc_sells_w = crypto_sells_w
											BTC = crypto_balance_array
											btc_trade_value_array = crypto_trade_value_array
											btc_level_array = crypto_level_array
											btc_level_value = crypto_level_value
											btc_opened_closed_array = crypto_opened_closed_array
											btc_trade_array = crypto_trade_array
											btc_max_level_value = crypto_max_level_value
											btc_min_level_value = crypto_min_level_value
											position.state = "OUT"
											global_grid.trade_bear()
											# global_grid.not_ready()
											print("Switch trends")
											print(crypto_balance)
										elif global_grid.trade_style == "BEAR GRID" :
										 	BTCDWN_sell_wager_array = (crypto_sell_wager_array)
										 	BTCDWN_wager_array = (crypto_wager_array)
										 	buy_wager = crypto_wager
										 	sell_wager = crypto_sell_wager
										 	BTCDWN_balance = crypto_balance
										 	BTCDWN_profit = crypto_profit
										 	df_BTCDWN_1m = df_crypto_1m
										 	df_BTCDWN_15m = df_crypto_15m
										 	df_BTCDWN_1d = df_crypto_1d
										 	df_BTCDWN_12h = df_crypto_12h
										 	btcdwn_sell_times_all = (crypto_sell_times_all)
										 	btcdwn_sell_times_even = (crypto_sell_times_even)
										 	btcdwn_buys_grid = (crypto_buys_grid)
										 	btcdwn_buy_times_grid = (crypto_buy_times_grid)
										 	btcdwn_sells_even = crypto_sells_even
										 	btcdwn_sells_all = (crypto_sells_all)
										 	btcdwn_sell_times_w = (crypto_sell_times_w)
										 	btcdwn_sells_w = (crypto_sells_w)
										 	BTCDWN = crypto_balance_array
										 	btcdwn_trade_value_array = crypto_trade_value_array
										 	btcdwn_level_value = crypto_level_value
										 	btcdwn_level_array = crypto_level_array
										 	btcdwn_opened_closed_array = crypto_opened_closed_array
										 	btcdwn_trade_array = crypto_trade_array
										 	btcdwn_max_level_value = crypto_max_level_value
										 	btcdwn_min_level_value = crypto_min_level_value
										 	position.state = "OUT"
										 	global_grid.trade_bull()
										 	print('switch trends')
									 		print(crypto_balance)
								# elif df_crypto_12h.iloc[index_12h]['STMA_1st_derivative'] < 0:
								if (df_crypto_1d.iloc[index_1d]["1dRSI"] < 55 and df_crypto_1d.iloc[index_1d]["Bol_band_width"] < 1 ) or (df_crypto_1d.iloc[index_1d]["1dRSI"] < 60 and df_crypto_1d.iloc[index_1d]["Bol_band_width"] > 1 ) :
									if df_crypto_1d.iloc[index_1d]["LTMA"] > df_crypto_1d.iloc[index_1d]["STMA"]:
										global_grid.wait_to_sell = "FALSE"
										print('pass')
										pass
									else:
										global_grid.made_first_trade = "FALSE"
										print('sell all bull')
										sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_balance_array, crypto_wager_array, -1)
										wins += len(np.where(np.array(crypto_opened_closed_array) == 0)[-1])
										closed_grid_trades += (len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]))
										print(closed_grid_trades)								
										for x in np.where(np.array(crypto_opened_closed_array) == 0)[-1] :
											closed_np_array = np.array(crypto_opened_closed_array)
											crypto_opened_closed_array.pop(x)
											crypto_opened_closed_array.insert(x, closed)
										USDT_profit = sell_action[0]
										sell_price = sell_action[1]
										crypto_balance = 0
										USDT_balance = USDT_balance + USDT_profit 
										USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
										crypto_sell_times_all.append(df_crypto_1m.iloc[cryp_counter]["index"])
										crypto_sells_all.append(df_crypto_1m.iloc[cryp_counter]["close"])
										sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
										crypto_balance_array.append(crypto_balance)
										usdt.append(USDT_balance)
										timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])									
										print("########################SELL-WIN-BUY AND SELL(switch trends-bull)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))									
										print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"WAGER:{crypto_balance_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
										print(f"1dRSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"TRADE NUMBER:{crypto_trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
										print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
										print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
										buy_sell_price = df_crypto_1m.iloc[cryp_counter]["close"]
										print(USDT_balance)
										global_grid.wait_to_sell = "FALSE"
										max_level_value = 0
										min_level_value = 0
										if global_grid.trade_style == "BULL GRID":
											BTC_sell_wager_array = (crypto_sell_wager_array)
											BTC_wager_array = (crypto_wager_array)
											buy_wager = crypto_wager 
											sell_wager = crypto_sell_wager 
											BTC_balance = crypto_balance 
											BTC_profit = crypto_profit 
											df_BTC_1d = df_crypto_1d 
											df_BTC_1m = df_crypto_1m 
											df_BTC_15m = df_crypto_15m
											df_BTC_12h = df_crypto_12h
											btc_sell_times_all = (crypto_sell_times_all)
											btc_sell_times_even = (crypto_sell_times_even)
											btc_buys_grid = (crypto_buys_grid)
											btc_buy_times_grid = (crypto_buy_times_grid)
											btc_sells_even = (crypto_sells_even)
											btc_sells_all = (crypto_sells_all)
											btc_sell_times_w = (crypto_sell_times_w)
											btc_sells_w = crypto_sells_w
											BTC = crypto_balance_array
											btc_trade_value_array = crypto_trade_value_array
											btc_level_array = crypto_level_array
											btc_level_value = crypto_level_value
											btc_opened_closed_array = crypto_opened_closed_array
											btc_trade_array = crypto_trade_array
											btc_max_level_value = crypto_max_level_value
											btc_min_level_value = crypto_min_level_value
											position.state = "OUT"
											global_grid.trade_bear()
											# global_grid.not_ready()
											print("Switch trends")
											print(crypto_balance)
										elif global_grid.trade_style == "BEAR GRID" :
										 	BTCDWN_sell_wager_array = (crypto_sell_wager_array)
										 	BTCDWN_wager_array = (crypto_wager_array)
										 	buy_wager = crypto_wager
										 	sell_wager = crypto_sell_wager
										 	BTCDWN_balance = crypto_balance
										 	BTCDWN_profit = crypto_profit
										 	df_BTCDWN_1m = df_crypto_1m
										 	df_BTCDWN_15m = df_crypto_15m
										 	df_BTCDWN_1d = df_crypto_1d
										 	df_BTCDWN_12h = df_crypto_12h
										 	btcdwn_sell_times_all = (crypto_sell_times_all)
										 	btcdwn_sell_times_even = (crypto_sell_times_even)
										 	btcdwn_buys_grid = (crypto_buys_grid)
										 	btcdwn_buy_times_grid = (crypto_buy_times_grid)
										 	btcdwn_sells_even = crypto_sells_even
										 	btcdwn_sells_all = (crypto_sells_all)
										 	btcdwn_sell_times_w = (crypto_sell_times_w)
										 	btcdwn_sells_w = (crypto_sells_w)
										 	BTCDWN = crypto_balance_array
										 	btcdwn_trade_value_array = crypto_trade_value_array
										 	btcdwn_level_value = crypto_level_value
										 	btcdwn_level_array = crypto_level_array
										 	btcdwn_opened_closed_array = crypto_opened_closed_array
										 	btcdwn_trade_array = crypto_trade_array
										 	btcdwn_max_level_value = crypto_max_level_value
										 	btcdwn_min_level_value = crypto_min_level_value
										 	position.state = "OUT"
										 	global_grid.trade_bull()
										 	print('switch trends')
										 	print(crypto_balance)
							elif  position.state == "IN" and df_crypto_1m.iloc[cryp_counter]['close'] > last_roof and global_grid.trade_style == "BEAR GRID":
								if df_crypto_1d.iloc[index_1d]["1dRSI"] < 59  :
									global_grid.made_first_trade = "FALSE"
									print('sell all bear')
									sell_action = sell_grid(df_crypto_1m.iloc[cryp_counter]["close"],crypto_balance_array, crypto_wager_array, -1)
									wins += len(np.where(np.array(crypto_opened_closed_array) == 0)[-1])
									closed_grid_trades += (len(np.where(np.array(crypto_opened_closed_array) == 0)[-1]))
									print(closed_grid_trades)								
									for x in np.where(np.array(crypto_opened_closed_array) == 0)[-1] :
										closed_np_array = np.array(crypto_opened_closed_array)
										crypto_opened_closed_array.pop(x)
										crypto_opened_closed_array.insert(x, closed)
									USDT_profit = sell_action[0]
									sell_price = sell_action[1]
									crypto_balance = 0
									USDT_balance = USDT_balance + USDT_profit 
									USDT_value = USDT_balance + crypto_balance * df_crypto_1m.iloc[cryp_counter]["close"]
									crypto_sell_times_all.append(df_crypto_1m.iloc[cryp_counter]["index"])
									crypto_sells_all.append(df_crypto_1m.iloc[cryp_counter]["close"])
									sells_grid.append(df_crypto_1m.iloc[cryp_counter]["close"])
									crypto_balance_array.append(crypto_balance)
									usdt.append(USDT_balance)
									timestamp.append(df_crypto_1m.iloc[cryp_counter]["timestamp"])	
									global_grid.wait_to_sell = "FALSE"																	
									print("########################SELL-WIN-BUY AND SELL(switch trends-bear)###########################",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"CRYPTO TRADING WITH:{crypto}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))									
									print(f"SELL-MINS-{df_crypto_1m.iloc[cryp_counter]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f'SELL_Price:{df_crypto_1m.iloc[cryp_counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"WAGER:{crypto_balance_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
									print(f"CRYPTO_Balance:{crypto_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
									print(f"1dRSI:{df_crypto_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"TRADE NUMBER:{crypto_trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
									print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
									print(f"LEVEL PRICE:{crypto_level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
									buy_sell_price = df_crypto_1m.iloc[cryp_counter]["close"]
									print(USDT_balance)
									max_level_value = 0
									min_level_value = 0
									if global_grid.trade_style == "BULL GRID":
										BTC_sell_wager_array = (crypto_sell_wager_array)
										BTC_wager_array = (crypto_wager_array)
										buy_wager = crypto_wager 
										sell_wager = crypto_sell_wager 
										BTC_balance = crypto_balance 
										BTC_profit = crypto_profit 
										df_BTC_1d = df_crypto_1d 
										df_BTC_1m = df_crypto_1m 
										df_BTC_15m = df_crypto_15m
										df_BTC_12h = df_crypto_12h
										btc_sell_times_all = (crypto_sell_times_all)
										btc_sell_times_even = (crypto_sell_times_even)
										btc_buys_grid = (crypto_buys_grid)
										btc_buy_times_grid = (crypto_buy_times_grid)
										btc_sells_even = (crypto_sells_even)
										btc_sells_all = (crypto_sells_all)
										btc_sell_times_w = (crypto_sell_times_w)
										btc_sells_w = crypto_sells_w
										BTC = crypto_balance_array
										btc_trade_value_array = crypto_trade_value_array
										btc_level_array = crypto_level_array
										btc_level_value = crypto_level_value
										btc_opened_closed_array = crypto_opened_closed_array
										btc_trade_array = crypto_trade_array										
										position.state = "OUT"
										global_grid.trade_bear()
										# global_grid.not_ready()
										print("Switch trends")
										print(crypto_balance)
									elif global_grid.trade_style == "BEAR GRID" :
									 	BTCDWN_sell_wager_array = (crypto_sell_wager_array)
									 	BTCDWN_wager_array = (crypto_wager_array)
									 	buy_wager = crypto_wager
									 	sell_wager = crypto_sell_wager
									 	BTCDWN_balance = crypto_balance
									 	BTCDWN_profit = crypto_profit
									 	df_BTCDWN_1m = df_crypto_1m
									 	df_BTCDWN_15m = df_crypto_15m
									 	df_BTCDWN_1d = df_crypto_1d
									 	df_BTCDWN_12h = df_crypto_12h
									 	btcdwn_sell_times_all = (crypto_sell_times_all)
									 	btcdwn_sell_times_even = (crypto_sell_times_even)
									 	btcdwn_buys_grid = (crypto_buys_grid)
									 	btcdwn_buy_times_grid = (crypto_buy_times_grid)
									 	btcdwn_sells_even = crypto_sells_even
									 	btcdwn_sells_all = (crypto_sells_all)
									 	btcdwn_sell_times_w = (crypto_sell_times_w)
									 	btcdwn_sells_w = (crypto_sells_w)
									 	BTCDWN = crypto_balance_array
									 	btcdwn_trade_value_array = crypto_trade_value_array
									 	btcdwn_level_value = crypto_level_value
									 	btcdwn_level_array = crypto_level_array	
									 	btcdwn_opened_closed_array = crypto_opened_closed_array
									 	btcdwn_trade_array = crypto_trade_array								 	
									 	position.state = "OUT"
									 	global_grid.trade_bull()
									 	print('switch trends')
									 	print(crypto_balance)




							# print('try to switch')



# At each level buy AND sell one "wager" unless the previous open trade is a loss. Then just buy until the price starts to increase



			if counter == 15:counter= 0; index_15m += 1

		except Exception as e:
			print(e)

	# 	plotter.cla()
	# 	plotter.plot(x,y)
	# 	if global_rising.roof != np.nan:
	# 		plotter.hlines(global_rising.roof,0,x[-1])
	# 	if global_rising.roof_2 != np.nan:
	# 		plotter.hlines(global_rising.roof_2,0,x[-1])

	# ani = animation.FuncAnimation(plotter.gcf(),animate,interval=10)
	# plotter.show()

	df_BTC_1d["PLOT_index"] = df_BTC_1m["index"] * 1440 
	df_BTC_15m["PLOT_index"] = df_BTC_1m["index"] * 15
	df_BTCDWN_1d["PLOT_index"] = df_BTCDWN_1d["index"] * 1440
	df_BTCDWN_15m["PLOT_index"] = df_BTCDWN_1m["index"] * 15

	if global_grid.trade_style == "BULL GRID" :
		BTC_balance = crypto_balance
	else:
		BTCDWN_balance = crypto_balance

	print(f"USDT_balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"BTC_balance:{BTC_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"BTCDWN_balance:{BTCDWN_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"USDT Value:{USDT_balance + (crypto_balance * df_crypto_1m.iloc[-1]['close'])}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
	print(f"Market Buys:{len(buys_market)}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"BTC Grid Buys:{len(btc_buys_grid)}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
	print(f"BTCDOWN Grid Buys:{len(btcdwn_buys_grid)}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))			
	print(f"OPENED:{opened_grid_trades}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
	print(f"wins:{wins}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"losses:{losses}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"Even trades:{out_even}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"CLOSED:{closed_grid_trades}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
	print(f'last price:{df_BTC_1m.tail(1)["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"USDT_balance:{USDT_balance}")
	print(f"BTC_balance:{BTC_balance}")
	print(f'BTCDWN_balance:{BTCDWN_balance}')
	print(f'Crypto balance:{crypto_balance}')
	print(f"USDT Value:{USDT_balance + (crypto_balance * df_crypto_1m.iloc[-1]['close'])}")
	print(f"Market Buys:{len(buys_market)}")
	print(f"BTC Grid Buys:{len(btc_buys_grid)}")
	print(f"BTCDOWN Grid Buys:{len(btcdwn_buys_grid)}")
	print(f"OPENED:{opened_grid_trades}")
	print(f"wins:{wins}")
	print(f"losses:{losses}")
	print(f"BTC Even trades:{len(btc_sells_even)}")
	print(f"BTCDOWN Even trades:{len(btcdwn_sells_even)}")
	print(f"CLOSED:{closed_grid_trades}")
	print(f'last price:{df_BTC_1m.tail(1)["close"]}')
	print(f'length df_BTC_1m:{len(df_BTC_1m)}')
	print(f'btc opened araray: {btc_opened_closed_array}')
	print(f'btcdwn opened araray: {btcdwn_opened_closed_array}')	
	graph_btc(start_date, end_date, df_BTC_1m["index"], df_BTC_1m["close"], btc_buy_times_grid, btc_buys_grid, btc_sell_times_l, btc_sells_l, btc_sell_times_w, btc_sells_w, df_BTC_1m["Upper_band"], df_BTC_1m["Lower_band"], 
		df_BTC_1m["STMA"], df_BTC_1d["1dRSI"], df_BTC_1d["PLOT_index"], df_BTC_1d["close"], df_BTC_1d["MACD"], df_BTC_1d["MACD_sig"], df_BTC_1d["MACD_difference"], df_BTC_1d["MACD_DIFF_MA"], buy_times_market, buys_market,
		sell_times_market, sells_market, market_change_bull, bull_change_times, df_BTC_15m["15mRSI"], df_BTC_15m["PLOT_index"], df_BTC_1d["Lower_band"], df_BTC_1d["Upper_band"], df_BTC_1d["BB_MA"], 
		df_BTC_1d["STMA"], df_BTC_1d["MACD_Alpha_difference"], df_BTC_1d["MACD_1st_derivative"], df_BTC_1d["MACD_2nd_derivative"], df_BTC_1d["MACD_MA"], df_BTC_1d["1st_der_MA"], btc_sells_even, btc_sell_times_even,
		btc_sells_all, btc_sell_times_all)
	graph_btcdwn(start_date, end_date, df_BTCDWN_1m["index"], df_BTCDWN_1m["close"], btcdwn_buy_times_grid, btcdwn_buys_grid, btcdwn_sell_times_l, btcdwn_sells_l, btcdwn_sell_times_w, btcdwn_sells_w, df_BTCDWN_1m["Upper_band"], df_BTCDWN_1m["Lower_band"], 
		df_BTCDWN_1m["STMA"], df_BTCDWN_1d["1dRSI"], df_BTCDWN_1d["PLOT_index"], df_BTCDWN_1d["close"], df_BTCDWN_1d["MACD"], df_BTCDWN_1d["MACD_sig"], df_BTCDWN_1d["MACD_difference"], df_BTCDWN_1d["MACD_DIFF_MA"], buy_times_market, buys_market,
		sell_times_market, sells_market, market_change_bull, bull_change_times, df_BTCDWN_15m["15mRSI"], df_BTCDWN_15m["PLOT_index"], df_BTCDWN_1d["Lower_band"], df_BTCDWN_1d["Upper_band"], df_BTCDWN_1d["BB_MA"], 
		df_BTCDWN_1d["STMA"], df_BTCDWN_1d["MACD_Alpha_difference"], df_BTCDWN_1d["MACD_1st_derivative"], df_BTCDWN_1d["MACD_2nd_derivative"], df_BTCDWN_1d["MACD_MA"], df_BTCDWN_1d["1st_der_MA"], btcdwn_sells_even, btcdwn_sell_times_even,
		btcdwn_sells_all, btcdwn_sell_times_all)
	not_closed = np.where(np.array(crypto_opened_closed_array) == 0)[-1]
	print(f'trades not closed: {not_closed}')
	print(f'sell all trades: {btc_sells_all    ,    btcdwn_sells_all}')
	print(f'sell all times: {btc_sell_times_all , btcdwn_sell_times_all}')
	# open (f'logs/{start_date}-{end_date}-output.txt')

sim()
