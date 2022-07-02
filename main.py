from threading import Thread
from datetime import datetime
from BinanceStream import Binance
from TrainPrediction import TrainPrediction
import Logger

logger = Logger.logging_start(True)

PAIR = "USDT"

bn = Binance()
tp = TrainPrediction()

intervals = ['1d', '4h', '1h', '30m', '15m', '5m', '1m']
ks = [3, 5, 7]
coins = ["BTC", "ETH", "LTC"]
predictcoins = ["BTC", "ETH", "LTC", "AVAX", "SOL"]

results = []

for interval in intervals:
    for k in ks:
        for coin in coins:
            for predictcoin in predictcoins:
                if coin == predictcoin: continue
                coin_candles = bn.get_candles(coin=coin, pair=PAIR, interval=interval, limit=1000)
                predict_coin_candles = bn.get_candles(coin=predictcoin, pair=PAIR, interval=interval, limit=1000)

                for i in range(1, len(coin_candles)):
                    x = coin_candles[i]
                    x[0] = datetime.utcfromtimestamp(x[0]/1000).strftime("%Y-%m-%d %H:%M:%S")
                    x[6] = datetime.utcfromtimestamp(x[6]/1000).strftime("%Y-%m-%d %H:%M:%S")
                    x.append(coin_candles[i-1][4])
                    x.append(tp.change(x[4], coin_candles[i-1][4]))
                del coin_candles[0]

                for i in range(1, len(predict_coin_candles)):
                    x = predict_coin_candles[i]
                    x[0] = datetime.utcfromtimestamp(x[0]/1000).strftime("%Y-%m-%d %H:%M:%S")
                    x[6] = datetime.utcfromtimestamp(x[6]/1000).strftime("%Y-%m-%d %H:%M:%S")
                    x.append(predict_coin_candles[i-1][4])
                    x.append(tp.change(x[4], predict_coin_candles[i-1][4]))
                del predict_coin_candles[0]

                for i in range(len(coin_candles)):
                    for n in range(len(coin_candles[i])):
                        try:
                            coin_candles[i][n] = float(coin_candles[i][n])
                        except:
                            pass

                for i in range(len(predict_coin_candles)):
                    for n in range(len(predict_coin_candles[i])):
                        try:
                            predict_coin_candles[i][n] = float(predict_coin_candles[i][n])
                        except:
                            pass

                coin_candles = tp.normalize_data(coin_candles)
                predict_coin_candles = tp.normalize_data(predict_coin_candles)

                predictions = []
                for candle in predict_coin_candles:
                    prediction = tp.PAGR(candle, coin_candles, k)
                    predictions.append(prediction)
                accuracy = tp.getAccuracy(predict_coin_candles, predictions)
                logger.info('Interval: ' + interval)
                logger.info('K: ' + str(k))
                logger.info('Coin: ' + coin+PAIR)
                logger.info('Predict Coin: ' + predictcoin+PAIR)
                logger.info('Accuracy: ' + repr(accuracy) + '%')
                logger.info('-------------------------')
                results.append([interval, k, coin, predictcoin, accuracy])
logger.warning("FINISHED CALCULATION")
best_accuracy = max([x[4] for x in results])
best_accuracy_details = [x for x in results if x[4] == best_accuracy][0]
logger.info("BEST RESULT DETAILS")
logger.info('Interval: ' + best_accuracy_details[0])
logger.info('K: ' + str(best_accuracy_details[1]))
logger.info('Coin: ' + best_accuracy_details[2])
logger.info('Predict Coin: ' + best_accuracy_details[3])
logger.info('Accuracy: ' + repr(best_accuracy_details[4]) + '%')
logger.info('-------------------------')