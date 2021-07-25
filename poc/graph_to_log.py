import matplotlib.pyplot as plotter
import data
import numpy as np
import pandas as pd
from os import path, mkdir


	# This function will check if the path is created on the host system and if it is not then it creates it so other
	# processes can proceed
def create_path_or_do_nothing(path_in_question):
	if not path.isdir(path_in_question):
		mkdir(path_in_question)

def graph_btc(start_date, end_date, time, price, buy_times, buys_grid, times_sold_for_loss, sells_l, times_sold_for_win, sells_w, df15mUpper, 
	df15mLower, df15m15MA, df1dRSI, time_d, price_d, MACD, Signal, MACDDiff, MACD_diff_MA, buy_times_market, buys_market, sell_times_market, sells_market, 
	market_change_bull, bull_change_times, df15mRSI, time_15m, df1dLower, df1dUpper, df1d15MA, df1dLTMA, MACD_Alpha_difference, MACD_1st_derivative,
	MACD_2nd_derivative, MACD_MA, MA_of_derivative, sells_even, sell_times_even, sells_all, sell_times_all):
	line_width = float(0.2)
	logs_directory = str('logs')
	create_path_or_do_nothing(logs_directory)
	pdf_file_name = str(f'{start_date}-{end_date}_BTC-output.pdf')
	pdf_file_output_path = str(path.join('/home/patty-o/TraderBot/Sim code/sim_rev19_GRID_BTCandBTCdwn_bullreturn/logs', pdf_file_name))

	blue = str('blue')
	green = str('green')
	red = str('red')
	purple = str('purple')
	black = str('black')
	yellow = str('yellow')
	orange = str('orange')

	plotter.figure(1, figsize=(30, 5))
	ax1 = plotter.subplot(611)
	plotter.grid(True, which='both')

	# Draw the current price, upper and lower Bollinger bands, and the moving average
	plotter.plot(time , price , color=blue, linewidth=line_width)
	plotter.plot(time , df15mUpper , color=green, linewidth=line_width)
	plotter.plot(time , df15mLower , color=green, linewidth=line_width)
	plotter.plot(time , df15m15MA , color=red, linewidth=line_width)

	# Draw the times the bot bought and sold (wins and loses)
	plotter.scatter(buy_times, buys_grid, color=purple, alpha=0.7, s=1.25)
	plotter.scatter(times_sold_for_loss, sells_l, color=red, alpha=0.7, s=1.25)
	plotter.scatter(times_sold_for_win, sells_w, color=green, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_even, sells_even, color=orange, alpha=0.7, s=1.25)		
	plotter.scatter(sell_times_all, sells_all, color=red, marker = 'x', alpha=1, s=2)
	plotter.scatter(buy_times_market, buys_market, color=black, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_market, sells_market, color=blue, alpha=0.7, s=1.25)
	plotter.scatter(bull_change_times, market_change_bull, color = black, alpha=0.7, s=1.25)

	plotter.subplot(612, sharex=ax1)
	plotter.grid(True, which='both')
	plotter.plot(time_d , price_d , color=blue, linewidth=line_width)
	plotter.plot(time_d , df1dUpper , color=green, linewidth=line_width)
	plotter.plot(time_d , df1dLower , color=green, linewidth=line_width)
	plotter.plot(time_d , df1d15MA , color=red, linewidth=line_width)
	plotter.plot(time_d , df1dLTMA , color=purple, linewidth=line_width)		

	# Draw the times the bot bought and sold (wins and loses)
	plotter.scatter(buy_times, buys_grid, color=purple, alpha=0.7, s=1.25)
	plotter.scatter(times_sold_for_loss, sells_l, color=red, alpha=0.7, s=1.25)
	plotter.scatter(times_sold_for_win, sells_w, color=green, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_even, sells_even, color=orange, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_all, sells_all, color=red, marker = 'x', alpha=1, s=2)		
	plotter.scatter(buy_times_market, buys_market, color=black, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_market, sells_market, color=blue, alpha=0.7, s=1.25)
	plotter.scatter(bull_change_times, market_change_bull, color = black, alpha=0.7, s=1.25)

	plotter.subplot(616, sharex=ax1)
	plotter.plot(time_15m, df15mRSI, color=black, linewidth=line_width)

	# pgo.Candlestick(open=df[''])
	plotter.subplot(613, sharex=ax1)
	plotter.plot(time_d , df1dRSI , color=black, linewidth=line_width)
	# plot.plot(time, 0.7, linestyle='dashed')
	# plot.plot(time, 0.3, linestyle='dashed')

	plotter.subplot(614, sharex = ax1)
	plotter.grid(True, which='both')
	plotter.bar(time_d, MACDDiff, align='center', alpha=0.5)
	plotter.plot(time_d, MACD, color=red, linewidth=line_width)
	plotter.plot(time_d, Signal, color=green, linewidth=line_width)
	plotter.plot(time_d, MACD_diff_MA, color=black, linewidth=line_width)

	ax2 = plotter.subplot(615, sharex=ax1)
	plotter.plot(time_d, MACD_diff_MA, color=red, linewidth=line_width)
	ax3 = ax2.twinx()
	ax3.plot(time_d, MACD_2nd_derivative, color=blue, linewidth=line_width)
	ax3.plot(time_d, MACD_1st_derivative, color=black, linewidth=line_width)
	ax3.plot(time_d, MA_of_derivative, '--', color=black, linewidth=line_width)		
	plotter.grid(True, which='both')

	# plotter.legend()

	return plotter.savefig(pdf_file_output_path, dpi=1500)



def graph_btcdwn(start_date, end_date, time, price, buy_times, buys_grid, times_sold_for_loss, sells_l, times_sold_for_win, sells_w, df15mUpper, 
	df15mLower, df15m15MA, df1dRSI, time_d, price_d, MACD, Signal, MACDDiff, MACD_diff_MA, buy_times_market, buys_market, sell_times_market, sells_market, 
	market_change_bull, bull_change_times, df15mRSI, time_15m, df1dLower, df1dUpper, df1d15MA, df1dLTMA, MACD_Alpha_difference, MACD_1st_derivative,
	MACD_2nd_derivative, MACD_MA, MA_of_derivative, sells_even, sell_times_even, sells_all, sell_times_all):
	line_width = float(0.2)
	logs_directory = str('logs')
	create_path_or_do_nothing(logs_directory)
	pdf_file_name = str(f'{start_date}-{end_date}_BTCDOWN-output.pdf')
	pdf_file_output_path = str(path.join('/home/patty-o/TraderBot/Sim code/sim_rev19_GRID_BTCandBTCdwn_bullreturn/logs', pdf_file_name))

	blue = str('blue')
	green = str('green')
	red = str('red')
	purple = str('purple')
	black = str('black')
	yellow = str('yellow')
	orange = str('orange')

	plotter.figure(2, figsize=(30, 5))
	bx1 = plotter.subplot(611)
	plotter.grid(True, which='both')

	# Draw the current price, upper and lower Bollinger bands, and the moving average
	bx1.plot(time , price , color=blue, linewidth=line_width)
	plotter.plot(time , df15mUpper , color=green, linewidth=line_width)
	plotter.plot(time , df15mLower , color=green, linewidth=line_width)
	plotter.plot(time , df15m15MA , color=red, linewidth=line_width)

	# Draw the times the bot bought and sold (wins and loses)
	plotter.scatter(buy_times, buys_grid, color=purple, alpha=0.7, s=1.25)
	plotter.scatter(times_sold_for_loss, sells_l, color=red, alpha=0.7, s=1.25)
	plotter.scatter(times_sold_for_win, sells_w, color=green, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_even, sells_even, color=orange, alpha=0.7, s=1.25)		
	plotter.scatter(sell_times_all, sells_all, color=red, marker = 'x', alpha=1, s=2)
	plotter.scatter(buy_times_market, buys_market, color=black, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_market, sells_market, color=blue, alpha=0.7, s=1.25)
	plotter.scatter(bull_change_times, market_change_bull, color = black, alpha=0.7, s=1.25)

	bx2 = plotter.subplot(612, sharex = bx1)
	plotter.grid(True, which='both')
	plotter.plot(time_d , price_d , color=blue, linewidth=line_width)
	plotter.plot(time_d , df1dUpper , color=green, linewidth=line_width)
	plotter.plot(time_d , df1dLower , color=green, linewidth=line_width)
	plotter.plot(time_d , df1d15MA , color=red, linewidth=line_width)
	plotter.plot(time_d , df1dLTMA , color=purple, linewidth=line_width)		

	# Draw the times the bot bought and sold (wins and loses)
	plotter.scatter(buy_times, buys_grid, color=purple, alpha=0.7, s=1.25)
	plotter.scatter(times_sold_for_loss, sells_l, color=red, alpha=0.7, s=1.25)
	plotter.scatter(times_sold_for_win, sells_w, color=green, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_even, sells_even, color=orange, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_all, sells_all, color=red, marker = 'x', alpha=1, s=2)		
	plotter.scatter(buy_times_market, buys_market, color=black, alpha=0.7, s=1.25)
	plotter.scatter(sell_times_market, sells_market, color=blue, alpha=0.7, s=1.25)
	plotter.scatter(bull_change_times, market_change_bull, color = black, alpha=0.7, s=1.25)

	# pgo.Candlestick(open=df[''])
	bx3 = plotter.subplot(613, sharex = bx2)
	plotter.plot(time_d , df1dRSI , color=black, linewidth=line_width)
	# plot.plot(time, 0.7, linestyle='dashed')
	# plot.plot(time, 0.3, linestyle='dashed')

	bx4 = plotter.subplot(614, sharex = bx3)
	plotter.grid(True, which='both')
	plotter.bar(time_d, MACDDiff, align='center', alpha=0.5)
	plotter.plot(time_d, MACD, color=red, linewidth=line_width)
	plotter.plot(time_d, Signal, color=green, linewidth=line_width)
	plotter.plot(time_d, MACD_diff_MA, color=black, linewidth=line_width)

	bx5 = plotter.subplot(615, sharex = bx4)
	plotter.plot(time_d, MACD_diff_MA, color=red, linewidth=line_width)
	bx55 = bx5.twinx()
	bx55.plot(time_d, MACD_2nd_derivative, color=blue, linewidth=line_width)
	bx55.plot(time_d, MACD_1st_derivative, color=black, linewidth=line_width)
	bx55.plot(time_d, MA_of_derivative, '--', color=black, linewidth=line_width)		
	plotter.grid(True, which='both')

	bx6 = plotter.subplot(616, sharex = bx5)
	plotter.plot(time_15m, df15mRSI, color=black, linewidth=line_width)

	# plotter.legend()

	return plotter.savefig(pdf_file_output_path, dpi=1500)