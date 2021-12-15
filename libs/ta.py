import numpy as np
import requests
import matplotlib.pyplot as plt

def na(src):
    copy = src.copy()
    copy = np.where(np.isnan(copy), True, False)
    return copy


def nz(src, number=0):
    copy = src.copy()
    copy = np.where(np.isnan(copy), number, copy)
    return copy


def fixnan(src):
    copy = src.copy()
    if np.isnan(copy[0]):
        copy[0] = 0
    for i, value in enumerate(copy):
        if np.isnan(value):
            copy[i] = copy[i - 1]
    return copy


def ema(data, span, selection = 0):

    copy = data.copy()
    if selection == 0:
        alpha = 2 / (span + 1.0)  # for pandas` span parameter
    elif selection == 1:
        alpha = 1 / (1.0 + span)  # for pandas` center-of-mass parameter
    elif selection == 2:
        alpha = 1 - np.exp(np.log(0.5) / span)  # for pandas` half-life parameter
    else:
        alpha = 1 / span

    alpha_rev = 1 - alpha
    n = copy.shape[0]

    pows = alpha_rev**(np.arange(n+1))

    scale_arr = 1 / pows[:-1]
    offset = copy[0] * pows[1:]
    pw0 = alpha*alpha_rev**(n-1)

    mult = copy*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    return out


def WMA(s, period):
    return np.roll(s,period).apply(lambda x: ((np.arange(period) + 1) * x).sum() / (np.arange(period) + 1).sum(),
                                   raw=True)


def HMA(s, period):
    return WMA(WMA(s, period // 2).multiply(2).sub(WMA(s, period)), int(np.sqrt(period)))


if __name__ == "__main__":
    klines = requests.get("https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=4h&limit=1000").json()
    klines = np.transpose(klines)
    klines = np.array(klines, dtype=np.float64)

    close = klines[4]
    test = np.array([3, 5, 6, 20, 25, 10, 15, 9])
    print(HMA(close,14))

    plt.plot(close[-100:], label='Close')
    plt.plot(ema(close,14)[-100:], label='EMA')
    plt.legend()
    plt.show()
