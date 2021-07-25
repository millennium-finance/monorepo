from pandas import DataFrame, concat, notnull
import math
from collections import deque
import numpy as np

'''
Simple Moving Average (S.M.A.)

SMA = Σ(i = 0, n = 11) / n + 1
'''


def simple_moving_average(periods):
    return sum(periods) / len(periods)


'''
Exponential Moving Average (E.M.A.)

EMA = (current period close - previous period EMA) * weighted multiplier + previous period EMA
                                                or 
EMA = (current period close * weighted multiplier) + previous period EMA * (1 - weighted multiplier)
'''


def exponential_moving_average(current_period_close, previous_period_ema, weighted_multiplier):
    return round(current_period_close * weighted_multiplier + previous_period_ema * (1 - weighted_multiplier), 4)


'''
Moving Average Convergence Divergence (M.A.C.D.) calculation

12 Day Weighted Multiplier = 2 / 13
26 Day Weighted Multiplier = 2 / 26    
'''


def moving_average_convergence_divergence(data_frame):
    close_column = 'close'
    Short_term_EMA = int(12)
    Long_term_EMA = int(24)
    weighted_multiplier_12 = 2 / 13
    weighted_multiplier_24 = 2 / 25

    close_column_array = data_frame[close_column].array

    first_Short_term_EMA_periods = close_column_array[0:(Short_term_EMA) - 1]
    first_Long_term_EMA_periods = close_column_array[0:(Long_term_EMA) - 1]

    sma_short = simple_moving_average(first_Short_term_EMA_periods)
    sma_long = simple_moving_average(first_Long_term_EMA_periods)

    ema_short = [sma_short]
    ema_long = [sma_long]

    for current_period_close in close_column_array[Short_term_EMA-1:Long_term_EMA - 2]:
        ema_short.append(exponential_moving_average(current_period_close, ema_short[-1], weighted_multiplier_12))

    for current_period_close in close_column_array[Long_term_EMA-1: -1]:
        ema_short.append(exponential_moving_average(current_period_close, ema_short[-1], weighted_multiplier_12))
        ema_long.append(exponential_moving_average(current_period_close, ema_long[-1], weighted_multiplier_24))

    data_frame_short = DataFrame({'Short_term_EMA': ema_short[11:]})
    data_frame_long = DataFrame({'Long_term_EMA': ema_long})
    return concat([data_frame_short, data_frame_long], axis=1)




def subtract_columns_by_row(row):
    return  subtract(row['Short_term_EMA'], row['Long_term_EMA'])




'''
Moving Average Convergence Divergence Signal (M.A.C.D. Signal)

This calculates the 9 period window of the MACD EMA's
'''


def moving_average_convergence_divergence_signal(data_frame):
    macd_column_name = str('MACD')
    macd_column = data_frame[macd_column_name].array
    weighted_multiplier_9 = 2 / 10

    ema_9 = simple_moving_average(macd_column[0:8])

    ema_9 = [ema_9]

    for current_macd_period in macd_column[9: -1]:
        if not math.isnan(current_macd_period):
            ema_9.append(exponential_moving_average(current_macd_period, ema_9[-1], weighted_multiplier_9))

    return DataFrame({'MACD_sig': ema_9})


'''
Simple subtraction
'''


def subtract(a, b):
    return a - b


def computeRSI(data, time_window):
    diff = data.diff().dropna()
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[diff > 0]
    down_chg[diff < 0] = diff[diff < 0]
    up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)
    return rsi


def computeRSI_15m(d, time_window):
    data = DataFrame({"rsi": d})
    diff = data.diff().dropna()
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[diff > 0]
    down_chg[diff < 0] = diff[diff < 0]
    up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)
    return rsi[-1:]

def three_pnt_reverse(y,y1,y2,y3):
    # dp/dt per minute
    h = 1
    derivative_first = (3*y-4*y1+y2)/(2*h) + 0*y3
    derivative_second = (2*y-5*y1+4*y2-y3)/(h^3)
    return derivative_first, derivative_second

def derivatives(data_frame):
    first_ders_a = []
    second_ders_a = []
    first_ders_b = []
    second_ders_b = []
    first_ders_c = []
    second_ders_c = []
    Index = 0
    a = deque(maxlen=4)
    b = deque(maxlen=4)
    c = deque(maxlen=4)
    for index, row in data_frame.iterrows():
        a.append(row["MACD_DIFF_MA"]) 
        b.append(row["LTMA"])
        c.append(row["STMA"])
        if len(a) != 4 :
            first_ders_a.append(np.nan) 
            second_ders_a.append(np.nan)        
        elif len(a) == 4 and len(b) != 4 :
            first_ders_a.append(three_pnt_reverse(a[3],a[2],a[1], a[0])[0])
            second_ders_a.append(three_pnt_reverse(a[3],a[2],a[1],a[0])[1])
            first_ders_b.append(np.nan) 
            second_ders_b.append(np.nan)
            first_ders_c.append(np.nan) 
            second_ders_c.append(np.nan)                                 
        elif len(a) == 4 and len(b) == 4: 
            first_ders_a.append(three_pnt_reverse(a[3],a[2],a[1], a[0])[0])
            second_ders_a.append(three_pnt_reverse(a[3],a[2],a[1],a[0])[1])
            first_ders_b.append(three_pnt_reverse(b[3],b[2],b[1], b[0])[0])
            second_ders_b.append(three_pnt_reverse(b[3],b[2],b[1],b[0])[1])
            first_ders_c.append(three_pnt_reverse(c[3],c[2],c[1], c[0])[0])
            second_ders_c.append(three_pnt_reverse(c[3],c[2],c[1],c[0])[1])            


    macd_ders_df = DataFrame({'MACD_1st_derivative':first_ders_a, 'MACD_2nd_derivative':second_ders_a})
    ma_ders_df = DataFrame({'LTMA_1st_derivative':first_ders_b, 'LTMA_2nd_derivative': second_ders_b})
    ST_ma_ders_df = DataFrame({'STMA_1st_derivative':first_ders_c, 'STMA_2nd_derivative':second_ders_c})
    return concat([macd_ders_df, ma_ders_df, ST_ma_ders_df], axis=1)

def MACD_difference_signal(row):
    return subtract(row['MACD'], row['MACD_sig'])

def Another_MACD_subtraction(row):
    return subtract(row['MACD'], row['MACD_DIFF_MA'])


def sort_frames(frame):
    return sorted(frame, key=notnull)


def bollinger_band_width(row):
    return (subtract(row['Lower_band'], row['Upper_band'])/row['BB_MA'])

def normalize_bbw(data_frame):
    norm_set = []
    max_difference = subtract(min(data_frame['Bol_band_width']),max(data_frame['Bol_band_width']))
    for index, row in data_frame.iterrows():
        local_difference = subtract(row['Bol_band_width'],min(data_frame['Bol_band_width']))
        norm_data = local_difference/max_difference
        norm_set.append(norm_data)
    norm_set = DataFrame({'Normalized_bbw':norm_set})
    return concat([norm_set], axis=1)

