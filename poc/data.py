from collections import deque

import pandas

import numpy as np

from binance_functions import create_binance_client, get_data_frame_BTC_1m, get_data_frame_BTC_15m, get_data_frame_BTC_1d, get_data_frame_BTCDWN_1m, get_data_frame_BTCDWN_1d, \
    get_data_frame_BTC_15m, get_data_frame_BTCDWN_12h, get_data_frame_BTC_12h
from functions import moving_average_convergence_divergence, moving_average_convergence_divergence_signal, exponential_moving_average, \
    computeRSI_15m, computeRSI, sort_frames, subtract_columns_by_row, MACD_difference_signal, Another_MACD_subtraction, derivatives, bollinger_band_width, normalize_bbw


def data_BTC_1m():
    binance_client = create_binance_client()
    data_frame_1m = get_data_frame_BTC_1m(binance_client)
    # data_frame_1m = pandas.read_csv("data/BTCUSDT_m_tempset.csv")


    ExMAs_1m = moving_average_convergence_divergence(data_frame_1m)
    data_frame_1m = pandas.concat([data_frame_1m, ExMAs_1m], axis=1)
    data_frame_1m["MACD"] = data_frame_1m.apply(subtract_columns_by_row, axis=1)
    MACD_sig_1m = moving_average_convergence_divergence_signal(data_frame_1m)
    data_frame_1m = pandas.concat([data_frame_1m, MACD_sig_1m], axis=1)
    data_frame_1m = data_frame_1m.apply(sort_frames)

    data_frame_1m["MACD_difference"] = data_frame_1m.apply(MACD_difference_signal, axis=1)
    data_frame_1m['MACD_DIFF_MA'] = data_frame_1m['MACD_difference'].rolling(window=3).mean()
    data_frame_1m["MACD_Alpha_difference"] = data_frame_1m.apply(Another_MACD_subtraction, axis=1)
    data_frame_1m['MACD_MA'] = data_frame_1m['MACD'].rolling(window=4).mean()
    # macd_derivative_1m = derivatives(data_frame_1m)
    # data_frame_1m = pandas.concat([data_frame_1m, macd_derivative_1m], axis=1)


    data_frame_1m['LTMA'] = data_frame_1m['close'].rolling(window=25).mean()
    data_frame_1m['STMA'] = data_frame_1m['close'].rolling(window=15).mean()
    data_frame_1m['BB_STD'] = data_frame_1m['close'].rolling(window=15).std()
    data_frame_1m['Upper_band'] = data_frame_1m['STMA'] + (data_frame_1m['BB_STD'] * 2.6)
    data_frame_1m['Lower_band'] = data_frame_1m['STMA'] - (data_frame_1m['BB_STD'] * 2.5)
    data_frame_1m["1mRSI"] = computeRSI(data_frame_1m["close"], 6)

    data_frame_1m['15mLTMA'] = data_frame_1m['close'].rolling(window=375).mean()
    data_frame_1m['15mBB_MA'] = data_frame_1m['close'].rolling(window=225).mean()
    data_frame_1m['15mBB_STD'] = data_frame_1m['close'].rolling(window=225).std()
    data_frame_1m['15mUpper'] = data_frame_1m['15mBB_MA'] + (data_frame_1m['15mBB_STD'] * 2.75)
    data_frame_1m['15mLower'] = data_frame_1m['15mBB_MA'] - (data_frame_1m['15mBB_STD'] * 3.25)

    data_frame_1m.to_csv("data_BTC/df_1m_BTC.csv")
    return data_frame_1m

def data_BTC_15m():
    binance_client = create_binance_client()
    data_frame_15m = get_data_frame_BTC_15m(binance_client)
    # data_frame_15m = pandas.read_csv("data/BTCUSDT_m_tempset.csv")    

    # data_frame_15m = data_frame_15m[["timestamp","close"]].iloc[::15, :].reset_index(drop=True)

    ExMAs_15m = moving_average_convergence_divergence(data_frame_15m)
    data_frame_15m = pandas.concat([data_frame_15m, ExMAs_15m], axis=1)
    data_frame_15m['MACD'] = data_frame_15m.apply(subtract_columns_by_row, axis=1)
    MACD_sig_15m = moving_average_convergence_divergence_signal(data_frame_15m)
    data_frame_15m = pandas.concat([data_frame_15m, MACD_sig_15m], axis=1)
    data_frame_15m = data_frame_15m.apply(sort_frames)

    data_frame_15m["MACD_difference"] = data_frame_15m.apply(MACD_difference_signal, axis=1)
    data_frame_15m['MACD_DIFF_MA'] = data_frame_15m['MACD_difference'].rolling(window=3).mean()
    data_frame_15m["MACD_Alpha_difference"] = data_frame_15m.apply(Another_MACD_subtraction, axis=1)
    data_frame_15m['MACD_MA'] = data_frame_15m['MACD'].rolling(window=3).mean()
    # macd_derivative_15m = derivatives(data_frame_15m)
    # data_frame_15m = pandas.concat([data_frame_15m, macd_derivative_15m], axis=1)

    data_frame_15m['LTMA'] = data_frame_15m['close'].rolling(window=50).mean()
    data_frame_15m['STMA'] = data_frame_15m['close'].rolling(window=20).mean()
    data_frame_15m['BB_STD'] = data_frame_15m['close'].rolling(window=20).std()
    data_frame_15m['Upper_band'] = data_frame_15m['STMA'] + (data_frame_15m['BB_STD'] * 2.75)
    data_frame_15m['Lower_band'] = data_frame_15m['STMA'] - (data_frame_15m['BB_STD'] * 3)
    data_frame_15m["15mRSI"] = computeRSI(data_frame_15m["close"], 6)

    data_frame_15m['15_15mLTMA'] = data_frame_15m['close'].rolling(window=375).mean()
    data_frame_15m['15_15mMA'] = data_frame_15m['close'].rolling(window=225).mean()
    data_frame_15m['15_15mSTD'] = data_frame_15m['close'].rolling(window=225).std()
    data_frame_15m['15_15mUpper'] = data_frame_15m['15_15mMA'] + (data_frame_15m['15_15mSTD'] * 2.6)
    data_frame_15m['15_15mLower'] = data_frame_15m['15_15mMA'] - (data_frame_15m['15_15mSTD'] * 2.75)

    data_frame_15m.to_csv("data_BTC/df_15m_BTC.csv")
    return data_frame_15m



def data_BTC_12h():
    binance_client = create_binance_client()
    data_frame_12h = get_data_frame_BTC_12h(binance_client)
    # data_frame_12h = pandas.read_csv("data/BTCUSDT_d_tempset.csv")    

    ExMAs_12h = moving_average_convergence_divergence(data_frame_12h)
    data_frame_12h = pandas.concat([data_frame_12h, ExMAs_12h], axis=1)
    data_frame_12h["MACD"] = data_frame_12h.apply(subtract_columns_by_row, axis=1)
    MACD_sig_12h = moving_average_convergence_divergence_signal(data_frame_12h)
    data_frame_12h = pandas.concat([data_frame_12h, MACD_sig_12h], axis=1)
    data_frame_12h = data_frame_12h.apply(sort_frames)

    data_frame_12h["MACD_difference"] = data_frame_12h.apply(MACD_difference_signal, axis=1)
    data_frame_12h['MACD_DIFF_MA'] = data_frame_12h['MACD_difference'].rolling(window=3).mean()
    data_frame_12h["MACD_Alpha_difference"] = data_frame_12h.apply(Another_MACD_subtraction, axis=1)
    data_frame_12h['MACD_MA'] = data_frame_12h['MACD'].rolling(window=3).mean()

    data_frame_12h['LTMA'] = data_frame_12h['close'].rolling(window=70).mean()
    data_frame_12h['STMA'] = data_frame_12h['close'].rolling(window=35).mean()
    macd_derivative_12h = derivatives(data_frame_12h)
    data_frame_12h = pandas.concat([data_frame_12h, macd_derivative_12h], axis=1)
    data_frame_12h['1st_der_MA'] = data_frame_12h['MACD_1st_derivative'].rolling(window=3).mean()

    data_frame_12h['BB_MA'] = data_frame_12h['close'].rolling(window=30).mean()
    data_frame_12h['BB_STD'] = data_frame_12h['close'].rolling(window=30).std()
    data_frame_12h['Upper_band'] = data_frame_12h['BB_MA'] + (data_frame_12h['BB_STD'] * 3.25)
    data_frame_12h['Lower_band'] = data_frame_12h['BB_MA'] - (data_frame_12h['BB_STD'] * 3.5)
    data_frame_12h["Bol_band_width"] = data_frame_12h.apply(bollinger_band_width, axis=1)
    normalized_bbw_12h =  normalize_bbw(data_frame_12h)
    data_frame_12h = pandas.concat([data_frame_12h, normalized_bbw_12h], axis=1)    
    data_frame_12h["12hRSI"] = computeRSI(data_frame_12h["close"], 6)
    data_frame_12h["12h_13period_RSI"] = computeRSI(data_frame_12h["close"], 13)
    data_frame_12h["12h_21period_RSI"] = computeRSI(data_frame_12h["close"], 21)
    data_frame_12h["12h_34period_RSI"] = computeRSI(data_frame_12h["close"], 34)

    data_frame_12h.to_csv("data_BTC/df_12h_BTC.csv")
    return data_frame_12h


def data_BTC_1d():
    binance_client = create_binance_client()
    data_frame_1d = get_data_frame_BTC_1d(binance_client)
    # data_frame_1d = pandas.read_csv("data/BTCUSDT_d_tempset.csv")    

    ExMAs_1d = moving_average_convergence_divergence(data_frame_1d)
    data_frame_1d = pandas.concat([data_frame_1d, ExMAs_1d], axis=1)
    data_frame_1d["MACD"] = data_frame_1d.apply(subtract_columns_by_row, axis=1)
    MACD_sig_1d = moving_average_convergence_divergence_signal(data_frame_1d)
    data_frame_1d = pandas.concat([data_frame_1d, MACD_sig_1d], axis=1)
    data_frame_1d = data_frame_1d.apply(sort_frames)

    data_frame_1d["MACD_difference"] = data_frame_1d.apply(MACD_difference_signal, axis=1)
    data_frame_1d['MACD_DIFF_MA'] = data_frame_1d['MACD_difference'].rolling(window=3).mean()
    data_frame_1d["MACD_Alpha_difference"] = data_frame_1d.apply(Another_MACD_subtraction, axis=1)
    data_frame_1d['MACD_MA'] = data_frame_1d['MACD'].rolling(window=3).mean()

    data_frame_1d['LTMA'] = data_frame_1d['close'].rolling(window=70).mean()
    data_frame_1d['STMA'] = data_frame_1d['close'].rolling(window=35).mean()
    macd_derivative_1d = derivatives(data_frame_1d)
    data_frame_1d = pandas.concat([data_frame_1d, macd_derivative_1d], axis=1)
    data_frame_1d['1st_der_MA'] = data_frame_1d['MACD_1st_derivative'].rolling(window=3).mean()

    data_frame_1d['BB_MA'] = data_frame_1d['close'].rolling(window=30).mean()
    data_frame_1d['BB_STD'] = data_frame_1d['close'].rolling(window=30).std()
    data_frame_1d['Upper_band'] = data_frame_1d['BB_MA'] + (data_frame_1d['BB_STD'] * 3.5)
    data_frame_1d['Lower_band'] = data_frame_1d['BB_MA'] - (data_frame_1d['BB_STD'] * 3.5)
    data_frame_1d["Bol_band_width"] = data_frame_1d.apply(bollinger_band_width, axis=1)
    normalized_bbw_1d =  normalize_bbw(data_frame_1d)
    data_frame_1d = pandas.concat([data_frame_1d, normalized_bbw_1d], axis=1)    
    data_frame_1d["1dRSI"] = computeRSI(data_frame_1d["close"], 6)
    data_frame_1d["1d_13period_RSI"] = computeRSI(data_frame_1d["close"], 13)
    data_frame_1d["1d_21period_RSI"] = computeRSI(data_frame_1d["close"], 21)
    data_frame_1d["1d_34period_RSI"] = computeRSI(data_frame_1d["close"], 34)

    data_frame_1d['15dLTMA'] = data_frame_1d['close'].rolling(window=375).mean()
    data_frame_1d['15dBB_MA'] = data_frame_1d['close'].rolling(window=225).mean()
    data_frame_1d['15dBB_STD'] = data_frame_1d['close'].rolling(window=225).std()
    data_frame_1d['15dUpper'] = data_frame_1d['15dBB_MA'] + (data_frame_1d['15dBB_STD'] * 2.6)
    data_frame_1d['15dLower'] = data_frame_1d['15dBB_MA'] - (data_frame_1d['15dBB_STD'] * 2.75)


    data_frame_1d.to_csv("data_BTC/df_1d_BTC.csv")
    return data_frame_1d






def data_BTCDWN_1m():
    binance_client = create_binance_client()
    data_frame_BTCDWN_1m = get_data_frame_BTCDWN_1m(binance_client)
    
    ExMAs_1m = moving_average_convergence_divergence(data_frame_BTCDWN_1m)
    data_frame_BTCDWN_1m = pandas.concat([data_frame_BTCDWN_1m, ExMAs_1m], axis=1)
    data_frame_BTCDWN_1m["MACD"] = data_frame_BTCDWN_1m.apply(subtract_columns_by_row, axis=1)
    MACD_sig_1m = moving_average_convergence_divergence_signal(data_frame_BTCDWN_1m)
    data_frame_BTCDWN_1m = pandas.concat([data_frame_BTCDWN_1m, MACD_sig_1m], axis=1)
    data_frame_BTCDWN_1m = data_frame_BTCDWN_1m.apply(sort_frames)

    data_frame_BTCDWN_1m["MACD_difference"] = data_frame_BTCDWN_1m.apply(MACD_difference_signal, axis=1)
    data_frame_BTCDWN_1m['MACD_DIFF_MA'] = data_frame_BTCDWN_1m['MACD_difference'].rolling(window=3).mean()
    data_frame_BTCDWN_1m["MACD_Alpha_difference"] = data_frame_BTCDWN_1m.apply(Another_MACD_subtraction, axis=1)
    data_frame_BTCDWN_1m['MACD_MA'] = data_frame_BTCDWN_1m['MACD'].rolling(window=4).mean()
    # macd_derivative_1m = derivatives(data_frame_BTCDWN_1m)
    # data_frame_BTCDWN_1m = pandas.concat([data_frame_BTCDWN_1m, macd_derivative_1m], axis=1)


    data_frame_BTCDWN_1m['LTMA'] = data_frame_BTCDWN_1m['close'].rolling(window=25).mean()
    data_frame_BTCDWN_1m['STMA'] = data_frame_BTCDWN_1m['close'].rolling(window=15).mean()
    data_frame_BTCDWN_1m['BB_STD'] = data_frame_BTCDWN_1m['close'].rolling(window=15).std()
    data_frame_BTCDWN_1m['Upper_band'] = data_frame_BTCDWN_1m['STMA'] + (data_frame_BTCDWN_1m['BB_STD'] * 2.6)
    data_frame_BTCDWN_1m['Lower_band'] = data_frame_BTCDWN_1m['STMA'] - (data_frame_BTCDWN_1m['BB_STD'] * 2.5)
    data_frame_BTCDWN_1m["1mRSI"] = computeRSI(data_frame_BTCDWN_1m["close"], 6)

    data_frame_BTCDWN_1m['15mLTMA'] = data_frame_BTCDWN_1m['close'].rolling(window=375).mean()
    data_frame_BTCDWN_1m['15mBB_MA'] = data_frame_BTCDWN_1m['close'].rolling(window=225).mean()
    data_frame_BTCDWN_1m['15mBB_STD'] = data_frame_BTCDWN_1m['close'].rolling(window=225).std()
    data_frame_BTCDWN_1m['15mUpper'] = data_frame_BTCDWN_1m['15mBB_MA'] + (data_frame_BTCDWN_1m['15mBB_STD'] * 2.75)
    data_frame_BTCDWN_1m['15mLower'] = data_frame_BTCDWN_1m['15mBB_MA'] - (data_frame_BTCDWN_1m['15mBB_STD'] * 3.25)

    data_frame_BTCDWN_1m.to_csv("data_BTCDWN/df_1m_BTCDWN.csv")
    return data_frame_BTCDWN_1m

def data_BTCDWN_15m():
    binance_client = create_binance_client()
    data_frame_BTCDWN_15m = get_data_frame_BTCDWN_1m(binance_client)
    
    data_frame_BTCDWN_15m = data_frame_BTCDWN_15m[["timestamp","close"]].iloc[::15, :].reset_index(drop=True)

    ExMAs_1m = moving_average_convergence_divergence(data_frame_BTCDWN_15m)
    data_frame_BTCDWN_15m = pandas.concat([data_frame_BTCDWN_15m, ExMAs_1m], axis=1)
    data_frame_BTCDWN_15m["MACD"] = data_frame_BTCDWN_15m.apply(subtract_columns_by_row, axis=1)
    MACD_sig_1m = moving_average_convergence_divergence_signal(data_frame_BTCDWN_15m)
    data_frame_BTCDWN_15m = pandas.concat([data_frame_BTCDWN_15m, MACD_sig_1m], axis=1)
    data_frame_BTCDWN_15m = data_frame_BTCDWN_15m.apply(sort_frames)

    data_frame_BTCDWN_15m["MACD_difference"] = data_frame_BTCDWN_15m.apply(MACD_difference_signal, axis=1)
    data_frame_BTCDWN_15m['MACD_DIFF_MA'] = data_frame_BTCDWN_15m['MACD_difference'].rolling(window=3).mean()
    data_frame_BTCDWN_15m["MACD_Alpha_difference"] = data_frame_BTCDWN_15m.apply(Another_MACD_subtraction, axis=1)
    data_frame_BTCDWN_15m['MACD_MA'] = data_frame_BTCDWN_15m['MACD'].rolling(window=4).mean()
    # macd_derivative_1m = derivatives(data_frame_BTCDWN_15m)
    # data_frame_BTCDWN_15m = pandas.concat([data_frame_BTCDWN_15m, macd_derivative_1m], axis=1)


    data_frame_BTCDWN_15m['LTMA'] = data_frame_BTCDWN_15m['close'].rolling(window=25).mean()
    data_frame_BTCDWN_15m['STMA'] = data_frame_BTCDWN_15m['close'].rolling(window=15).mean()
    data_frame_BTCDWN_15m['BB_STD'] = data_frame_BTCDWN_15m['close'].rolling(window=15).std()
    data_frame_BTCDWN_15m['Upper_band'] = data_frame_BTCDWN_15m['STMA'] + (data_frame_BTCDWN_15m['BB_STD'] * 2.6)
    data_frame_BTCDWN_15m['Lower_band'] = data_frame_BTCDWN_15m['STMA'] - (data_frame_BTCDWN_15m['BB_STD'] * 2.5)
    data_frame_BTCDWN_15m["15mRSI"] = computeRSI(data_frame_BTCDWN_15m["close"], 6)

    data_frame_BTCDWN_15m['15mLTMA'] = data_frame_BTCDWN_15m['close'].rolling(window=375).mean()
    data_frame_BTCDWN_15m['15mBB_MA'] = data_frame_BTCDWN_15m['close'].rolling(window=225).mean()
    data_frame_BTCDWN_15m['15mBB_STD'] = data_frame_BTCDWN_15m['close'].rolling(window=225).std()
    data_frame_BTCDWN_15m['15mUpper'] = data_frame_BTCDWN_15m['15mBB_MA'] + (data_frame_BTCDWN_15m['15mBB_STD'] * 2.75)
    data_frame_BTCDWN_15m['15mLower'] = data_frame_BTCDWN_15m['15mBB_MA'] - (data_frame_BTCDWN_15m['15mBB_STD'] * 3.25)

    data_frame_BTCDWN_15m.to_csv("data_BTCDWN/df_15m_BTCDWN.csv")
    return data_frame_BTCDWN_15m


def data_BTCDWN_12h():
    binance_client = create_binance_client()
    data_frame_BTCDWN_12h = get_data_frame_BTCDWN_12h(binance_client)

    ExMAs_12h = moving_average_convergence_divergence(data_frame_BTCDWN_12h)
    data_frame_BTCDWN_12h = pandas.concat([data_frame_BTCDWN_12h, ExMAs_12h], axis=1)
    data_frame_BTCDWN_12h["MACD"] = data_frame_BTCDWN_12h.apply(subtract_columns_by_row, axis=1)
    MACD_sig_12h = moving_average_convergence_divergence_signal(data_frame_BTCDWN_12h)
    data_frame_BTCDWN_12h = pandas.concat([data_frame_BTCDWN_12h, MACD_sig_12h], axis=1)
    data_frame_BTCDWN_12h = data_frame_BTCDWN_12h.apply(sort_frames)

    data_frame_BTCDWN_12h["MACD_difference"] = data_frame_BTCDWN_12h.apply(MACD_difference_signal, axis=1)
    data_frame_BTCDWN_12h['MACD_DIFF_MA'] = data_frame_BTCDWN_12h['MACD_difference'].rolling(window=3).mean()
    data_frame_BTCDWN_12h["MACD_Alpha_difference"] = data_frame_BTCDWN_12h.apply(Another_MACD_subtraction, axis=1)
    data_frame_BTCDWN_12h['MACD_MA'] = data_frame_BTCDWN_12h['MACD'].rolling(window=3).mean()

    data_frame_BTCDWN_12h['LTMA'] = data_frame_BTCDWN_12h['close'].rolling(window=70).mean()
    data_frame_BTCDWN_12h['STMA'] = data_frame_BTCDWN_12h['close'].rolling(window=35).mean()
    macd_derivative_12h = derivatives(data_frame_BTCDWN_12h)
    data_frame_BTCDWN_12h = pandas.concat([data_frame_BTCDWN_12h, macd_derivative_12h], axis=1)
    data_frame_BTCDWN_12h['1st_der_MA'] = data_frame_BTCDWN_12h['MACD_1st_derivative'].rolling(window=3).mean()

    data_frame_BTCDWN_12h['BB_MA'] = data_frame_BTCDWN_12h['close'].rolling(window=30).mean()
    data_frame_BTCDWN_12h['BB_STD'] = data_frame_BTCDWN_12h['close'].rolling(window=30).std()
    data_frame_BTCDWN_12h['Upper_band'] = data_frame_BTCDWN_12h['BB_MA'] + (data_frame_BTCDWN_12h['BB_STD'] * 3.25)
    data_frame_BTCDWN_12h['Lower_band'] = data_frame_BTCDWN_12h['BB_MA'] - (data_frame_BTCDWN_12h['BB_STD'] * 3.5)
    data_frame_BTCDWN_12h["Bol_band_width"] = data_frame_BTCDWN_12h.apply(bollinger_band_width, axis=1) 
    normalized_bbw_12h =  normalize_bbw(data_frame_BTCDWN_12h)
    data_frame_BTCDWN_12h = pandas.concat([data_frame_BTCDWN_12h, normalized_bbw_12h], axis=1)
    data_frame_BTCDWN_12h["12hRSI"] = computeRSI(data_frame_BTCDWN_12h["close"], 6)
    data_frame_BTCDWN_12h["12h_8period_RSI"] = computeRSI(data_frame_BTCDWN_12h["close"], 8)
    data_frame_BTCDWN_12h["12h_13period_RSI"] = computeRSI(data_frame_BTCDWN_12h["close"], 13)
    data_frame_BTCDWN_12h["12h_21period_RSI"] = computeRSI(data_frame_BTCDWN_12h["close"], 21)


    data_frame_BTCDWN_12h.to_csv("data_BTCDWN/df_12h_BTCDWN.csv")
    return data_frame_BTCDWN_12h



def data_BTCDWN_1d():
    binance_client = create_binance_client()
    data_frame_BTCDWN_1d = get_data_frame_BTCDWN_1d(binance_client)

    ExMAs_1d = moving_average_convergence_divergence(data_frame_BTCDWN_1d)
    data_frame_BTCDWN_1d = pandas.concat([data_frame_BTCDWN_1d, ExMAs_1d], axis=1)
    data_frame_BTCDWN_1d["MACD"] = data_frame_BTCDWN_1d.apply(subtract_columns_by_row, axis=1)
    MACD_sig_1d = moving_average_convergence_divergence_signal(data_frame_BTCDWN_1d)
    data_frame_BTCDWN_1d = pandas.concat([data_frame_BTCDWN_1d, MACD_sig_1d], axis=1)
    data_frame_BTCDWN_1d = data_frame_BTCDWN_1d.apply(sort_frames)

    data_frame_BTCDWN_1d["MACD_difference"] = data_frame_BTCDWN_1d.apply(MACD_difference_signal, axis=1)
    data_frame_BTCDWN_1d['MACD_DIFF_MA'] = data_frame_BTCDWN_1d['MACD_difference'].rolling(window=3).mean()
    data_frame_BTCDWN_1d["MACD_Alpha_difference"] = data_frame_BTCDWN_1d.apply(Another_MACD_subtraction, axis=1)
    data_frame_BTCDWN_1d['MACD_MA'] = data_frame_BTCDWN_1d['MACD'].rolling(window=3).mean()

    data_frame_BTCDWN_1d['LTMA'] = data_frame_BTCDWN_1d['close'].rolling(window=70).mean()
    data_frame_BTCDWN_1d['STMA'] = data_frame_BTCDWN_1d['close'].rolling(window=35).mean()
    macd_derivative_1d = derivatives(data_frame_BTCDWN_1d)
    data_frame_BTCDWN_1d = pandas.concat([data_frame_BTCDWN_1d, macd_derivative_1d], axis=1)
    data_frame_BTCDWN_1d['1st_der_MA'] = data_frame_BTCDWN_1d['MACD_1st_derivative'].rolling(window=3).mean()

    data_frame_BTCDWN_1d['BB_MA'] = data_frame_BTCDWN_1d['close'].rolling(window=30).mean()
    data_frame_BTCDWN_1d['BB_STD'] = data_frame_BTCDWN_1d['close'].rolling(window=30).std()
    data_frame_BTCDWN_1d['Upper_band'] = data_frame_BTCDWN_1d['BB_MA'] + (data_frame_BTCDWN_1d['BB_STD'] * 3.5)
    data_frame_BTCDWN_1d['Lower_band'] = data_frame_BTCDWN_1d['BB_MA'] - (data_frame_BTCDWN_1d['BB_STD'] * 3.5)
    data_frame_BTCDWN_1d["Bol_band_width"] = data_frame_BTCDWN_1d.apply(bollinger_band_width, axis=1) 
    normalized_bbw_1d =  normalize_bbw(data_frame_BTCDWN_1d)
    data_frame_BTCDWN_1d = pandas.concat([data_frame_BTCDWN_1d, normalized_bbw_1d], axis=1)
    data_frame_BTCDWN_1d["1dRSI"] = computeRSI(data_frame_BTCDWN_1d["close"], 6)
    data_frame_BTCDWN_1d["1d_8period_RSI"] = computeRSI(data_frame_BTCDWN_1d["close"], 8)
    data_frame_BTCDWN_1d["1d_13period_RSI"] = computeRSI(data_frame_BTCDWN_1d["close"], 13)
    data_frame_BTCDWN_1d["1d_21period_RSI"] = computeRSI(data_frame_BTCDWN_1d["close"], 21)

    data_frame_BTCDWN_1d.to_csv("data_BTCDWN/df_1d_BTCDWN.csv")
    return data_frame_BTCDWN_1d
