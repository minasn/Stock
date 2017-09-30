import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mat
import copy


def CandleStickPlot(ax, Date, Open, Close, High, Low):
    #文件名：蜡烛图

    #处理停牌日期，停牌日O/H/L均为停滞收盘价
    for i in np.arange(len(Close)):
        if Open[i]== 0:
            Open[i]=Close[i]
            High[i]=Close[i]
            Low[i]=Close[i]
        else:
            pass
    #处理K线矩形部分
    #上涨，飘红，在上涨时候，收盘价大于开盘价，设置上边数据为收盘价，下边数据为开盘价，将相反数us何止为nan
    upClose=copy.deepcopy(Close)
    upClose[Close<=Open]=np.nan
    upOpen=copy.deepcopy(Open)
    upOpen[Close<=Open]=np.nan
    #下跌，飘绿
    downClose=copy.deepcopy(Close)
    downClose[Close>=Open]=np.nan
    downOpen=copy.deepcopy(Open)
    downOpen[Close>=Open]=np.nan
    #横盘
    openEqualClose=copy.deepcopy(Close)
    openEqualClose[Close!=Open]=np.nan

    #设置x轴坐标对应的y轴数据，使用nan作为间隔
    #设置path 左下 右下 右上 左上 空
    xAxisNan=np.array(np.arange(0,len(Close)))+np.nan
    rectangleRed=np.array([upOpen,upOpen,upClose,upClose,xAxisNan])#line_nan，空隙
    rectangleRed=np.ravel(rectangleRed,'F')#ravel 平坦化数组
    rectangleGreen=np.array([downClose,downClose,downOpen,downOpen,xAxisNan])
    rectangleGreen=np.ravel(rectangleGreen,'F')
    rectangleEqual=np.array([openEqualClose,openEqualClose,openEqualClose,openEqualClose,xAxisNan])
    rectangleEqual=np.ravel(rectangleEqual,'F')
    #x轴坐标
    xAxis=np.array(np.arange(0,len(Close)))
    xAxisLeft=xAxis-0.25
    xAxisRight=xAxis+0.25
    rectangleXAxis=np.array([xAxisLeft,xAxisRight,xAxisRight,xAxisLeft,xAxisNan])
    rectangleXAxis=np.ravel(rectangleXAxis,'F')
    rectangleRed = np.array([rectangleXAxis, rectangleRed]).T
    rectangleGreen = np.array([rectangleXAxis, rectangleGreen]).T
    rectangleEqual = np.array([rectangleXAxis, rectangleEqual]).T
    rectangleRed = mat.patches.Polygon(rectangleRed, color='r', zorder=1)
    rectangleGreen = mat.patches.Polygon(rectangleGreen, color='g', zorder=1)
    rectangleEqual = mat.patches.Polygon(rectangleEqual, color='k', zorder=1)

    # 影线
    #  Length = len(Close)
    xAxis = np.array(np.arange(0, len(Close)))
    highPrice = copy.deepcopy(Close)
    highPrice[Close < Open] = Open[Close < Open]
    lowPrice = copy.deepcopy(Close)
    lowPrice[Close > Open] = Open[Close > Open]
    lineRed = np.array([High, highPrice, xAxisNan])
    lineRed = np.ravel(lineRed, 'F')
    lineGreen = np.array([Low, lowPrice, xAxisNan])
    lineGreen = np.ravel(lineGreen, 'F')
    lineXAxis = np.array([xAxis, xAxis, xAxis])
    lineXAxis = np.ravel(lineXAxis, 'F')
    lineRed = mat.lines.Line2D(lineXAxis, lineRed, color='r', linestyle='solid', zorder=0)
    lineGreen = mat.lines.Line2D(lineXAxis, lineGreen, color='g', linestyle='solid', zorder=0)#
    #  绘制矩形
    #  fig = plt.figure(figsize=(len(Close)//5, 10))
    ax = plt.subplot(111)
    ax.add_patch(rectangleRed)
    ax.add_patch(rectangleGreen)
    ax.add_patch(rectangleEqual)
    ax.add_line(lineRed)
    ax.add_line(lineGreen)
    ll = Low.min() * 0.997
    hh = High.max() * 1.003
    length = len(Close)
    v = [-2, length + 2, ll, hh]
    ax.set_title(str('002743'))
    plt.axis(v)
    ax.set_xticklabels(Date)
    ax.set_xticks(np.linspace(0, len(Close) - 1, len(Date)))
    ax.grid(linewidth=0.5)
    plt.setp(plt.gca().get_xticklabels(),rotation=90,horizontalalignment='center')
    plt.show()

gp=ts.get_k_data('002743')
open=gp['open']
close=gp['close']
high=gp['high']
low=gp['low']
date=gp['date']

fig=plt.figure(figsize=(16,9))
ax=fig.add_subplot()
CandleStickPlot(ax=ax,Date=date,Open=open,Close=close,High=high,Low=low)