import data
import os
import shutil
import numpy as np
from datetime import datetime
from os import path, mkdir
import pandas


# Print critical information for each buy and sell execution in bot.py

def create_path_or_do_nothing(path_in_question):
	if not path.isdir(path_in_question):
		mkdir(path_in_question)
	# Execute print for short trade purchase

# file path
pdf_file_output_path = str(path.join('/home/patty-o/TraderBot/Sim code/sim_rev14.1_longtermstrategy_BTC_dynamic_grid_open_close/logs', pdf_file_name))
# create path and define file 
logs_directory = str('logs')
create_path_or_do_nothing(logs_directory)
pdf_file_name = str(f'{start_date}-{end_date}-output.txt')

def print_market_buy(close, time, df_1d):
	# shutil.rmtree('logs')
	# os.mkdir("logs")

	print(f"BUY-MINS-{time}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"Bought from closing data from:{df_1d.iloc[index_1d]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'BUY_Price:{close}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"BTC_Balance:{BTC_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'RSI:{df_1d.iloc[index_1d]["1dRSI"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'MACD_diff:{df_1d.iloc[index_macd]["MACD_difference"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'Short_action_diff:{Short_action_diff}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
	print(f'MACD_sig:{df_1d.iloc[index_macd]["MACD_sig"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'Short_moving_average(35-days):{df_1d.iloc[index_1d]["1dSTMA"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'Long_moving_average(70-days):{df_1d.iloc[index_1d]["1dLTMA"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'buy_line_derivative:{df_1d.iloc[index_1d]["LTMA_1st_derivative"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))

	# return 	pandas.append(path.join('logs', pdf_file_name))


def print_market_sell(close, time, df_1d):
	print(f"SELL-MINS-{time}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"Sold from closing data from:{df_1d.iloc[index_1d]['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'SELL_Price:{close}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"wins:{wins}")
	print(f"losses:{losses}")
	print(f'RSI:{df_1d.iloc[index_1d]["1dRSI"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'Current_MACD_diff:{df_1d.iloc[index_macd]["MACD_difference"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'Last_MACD_diff:{df_1d.iloc[index_1d]["MACD_difference"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'Short_action_diff:{Short_action_diff}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
	print(f'MACD_sig:{df_1d.iloc[index_macd]["MACD_sig"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'MACD_2nd_derivative:{df_1d.iloc[index_macd]["MACD_2nd_derivative"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))	
	# return	pandas.append(path.join('logs', pdf_file_name))


def print_grid_buy(close, time, df_1d):
	print(f"BUY-MINS-{row['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'BUY_Price:{row["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'BTCDWN_Price:{df_1m_dwn.iloc[counter]["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"BTC_Balance:{BTC_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))							
	# print(f"MARKET VALUE:{market_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"RSI:{df_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"WAGER:{buy_wager_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"TRADE NUMBER:{trade_array[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
	print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"LEVEL PRICE:{level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))

def print_grid_sell_even(close, time, df_1d, trade_number):
	print(f"SELL-MINS-{row['timestamp']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f'SELL_Price:{row["close"]}',file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"WAGER:{buy_net[trade_number_open]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
	print(f"EVEN TRADES:{out_even}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))							
	print(f"BTC_Balance:{BTC_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"USDT_Balance:{USDT_balance}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"USDT VALUE:{USDT_value}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"TRADE PROFIT:{trade_profit}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))								
	print(f"RSI:{df_1d.iloc[index_1d]['1dRSI']}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"TRADE NUMBER:{trade_number_open}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))						
	print(f"LEVEL:{trade_level}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))
	print(f"LEVEL PRICE:{level_value[-1]}",file=open(f'logs/{start_date}-{end_date}-output.txt', 'a'))