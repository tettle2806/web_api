"""Мы будем работать в ТФ 5 минут.
Используется две кривые тренда.
Если быстрая скольящая средняя выше медленного скользящего среднего, то тренд восходящий.
И используем края полосы боллинджера для определения точек входа в позу."""


import numpy as np
import pandas as pd
import pandas_ta as ta
from backtesting import Strategy, Backtest
from pygments.lexers import go
from tqdm import tqdm

df = pd.read_csv("EURUSD_Candlestick_5_M_ASK_30.09.2019-30.09.2022.csv")

# Убираем милисекунды, которые нам не нужны.
df["Gmt time"]=df["Gmt time"].str.replace(".000","")

#Преобразуем дату и время, которые нам теперь не нужны.
df['Gmt time']=pd.to_datetime(df['Gmt time'],format='%d.%m.%Y %H:%M:%S')

#Фильтрация свечей выходных дней
df=df[df.High!=df.Low]
df.set_index("Gmt time", inplace=True)

#Создаём две скользящие средние, пересечение которых и будет говорить нам о том, стоит ли нам открывать позицию или нет.
df["EMA_slow"]=ta.ema(df.Close, length=50)
df["EMA_fast"]=ta.ema(df.Close, length=30)
df['RSI']=ta.rsi(df.Close, length=10)

#Вычисляем полосы боллинджера
my_bbands = ta.bbands(df.Close, length=15, std=1.5)

#Параметр ATR позволяет нам определить расстояния стопов и ТП.
df['ATR']=ta.atr(df.High, df.Low, df.Close, length=7)
df=df.join(my_bbands)
print(df)

def ema_signal(df, current_candle, backcandles):
    df_slice = df.reset_index().copy()
    # Получаем диапазон свечей для определения тренда.
    start = max(0, current_candle - backcandles)
    end = current_candle
    relevant_rows = df_slice.iloc[start:end]

    # Проверяем, находится ли скользящая средняя выше или ниже другой.
    if all(relevant_rows["EMA_fast"] < relevant_rows["EMA_slow"]):
        return 1
    elif all(relevant_rows["EMA_fast"] > relevant_rows["EMA_slow"]):
        return 2
    else:
        return 0


df=df[-30000:-1]
tqdm.pandas()
df.reset_index(inplace=True)
#Добавляем эту функцию в качестве нового столбца в нашу таблицу
df['EMASignal'] = df.progress_apply(lambda row: ema_signal(df, row.name, 7) , axis=1) #if row.name >= 20 else 0


def total_signal(df, current_candle, backcandles):
    #Если ума сигнал равен двум, то имеем сигнал на лонг.
    if (ema_signal(df, current_candle, backcandles) == 2
    #ждём пока полоса ема закроется ниже боллинджера.
            and df.Close[current_candle] <= df['BBL_15_1.5'][current_candle]

    ):
        #если всё ок, то получаем сигнал на лонг и возвращаем 2
        return 2
    if (ema_signal(df, current_candle, backcandles) == 1
            and df.Close[current_candle] >= df['BBU_15_1.5'][current_candle]
    ):
        return 1
    return 0

#Собрали данные за три месяца и сохраняем всё в общий сигнал. На выходе получаем 1 в тотал сигнал = позиция в шорт. 2 в лонг.
df['TotalSignal'] = df.progress_apply(lambda row: total_signal(df, row.name, 7), axis=1)

def pointpos(x):
    if x['TotalSignal']==2:
        return x['Low']-1e-3
    elif x['TotalSignal']==1:
        return x['High']+1e-3
    else:
        return np.nan

df['pointpos'] = df.apply(lambda row: pointpos(row), axis=1)

st=100
dfpl = df[st:st+350]
#dfpl.reset_index(inplace=True)
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close']),

                go.Scatter(x=dfpl.index, y=dfpl['BBL_15_1.5'],
                           line=dict(color='green', width=1),
                           name="BBL"),
                go.Scatter(x=dfpl.index, y=dfpl['BBU_15_1.5'],
                           line=dict(color='green', width=1),
                           name="BBU"),
                go.Scatter(x=dfpl.index, y=dfpl['EMA_fast'],
                           line=dict(color='black', width=1),
                           name="EMA_fast"),
                go.Scatter(x=dfpl.index, y=dfpl['EMA_slow'],
                           line=dict(color='blue', width=1),
                           name="EMA_slow")])

fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
                marker=dict(size=5, color="MediumPurple"),
                name="entry")

fig.show()

def SIGNAL():
    return df.TotalSignal


class MyStrat(Strategy):
    mysize = 3000
    slcoef = 1.1
    TPSLRatio = 1.5
    rsi_length = 16

    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)
        # df['RSI']=ta.rsi(df.Close, length=self.rsi_length)

    def next(self):
        super().next()
        slatr = self.slcoef * self.data.ATR[-1]
        TPSLRatio = self.TPSLRatio

        # if len(self.trades)>0:
        #     if self.trades[-1].is_long and self.data.RSI[-1]>=90:
        #         self.trades[-1].close()
        #     elif self.trades[-1].is_short and self.data.RSI[-1]<=10:
        #         self.trades[-1].close()

        if self.signal1 == 2 and len(self.trades) == 0:
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr * TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)

        elif self.signal1 == 1 and len(self.trades) == 0:
            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr * TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)


bt = Backtest(df, MyStrat, cash=250, margin=1 / 30)
print(bt.run())
bt.plot()