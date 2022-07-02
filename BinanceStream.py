import unicorn_binance_websocket_api, logging, math, os, requests, sys, time, threading, unicorn_binance_rest_api
from unicorn_fy.unicorn_fy import UnicornFy
from datetime import datetime
import pandas as pd

class Binance:
    def __init__(self, StreamHandler=None):
        self.channels = {'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_2h', 'kline_4h',
            'kline_6h', 'kline_8h', 'kline_12h', 'kline_1d', 'kline_3d', 'kline_1w', 'kline_1M'}
        logging.getLogger("unicorn_binance_websocket_api")
        #self.SH = StreamHandler()
        
    def run_stream(self):
        ssd = self.start_stream_data()
        rms = self.run_market_subscriptions()
        self.start_while()
        
    def get_candles(self, coin:str, pair:str, interval:str, limit=500, start=None):
        self.interval = interval
        url = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + coin.upper()+ pair.upper() + '&interval=' + interval + '&limit=' + str(limit)
        if not start == None:
            time = str(round(datetime.timestamp(datetime.strptime(start,"%m-%d-%Y"))) * 1000)
            url+= '&startTime='+ time
        klines = requests.get(url).json()
        # ['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', 'Quote asset volume', 'Number of trades','Taker by base', 'Taker buy quote', 'Ignore']
        return klines
    
    def start_stream_data(self, debug):
        try:
            self.ubra = unicorn_binance_rest_api.BinanceRestApiManager("", "")
        except requests.exceptions.ConnectionError:
            print("No internet connection?")
            sys.exit(1)

        self.ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(high_performance=True, debug=debug)

        worker_thread = threading.Thread(target=self.print_stream_data_from_stream_buffer, args=(self.ubwa,))
        worker_thread.start()
        return True
            
    def run_market_subscriptions(self):
        markets = []
        data = self.ubra.get_all_tickers()
        for item in data:
            markets.append(item['symbol'])

        divisor = math.ceil(len(markets) / self.ubwa.get_limit_of_subscriptions_per_stream())
        max_subscriptions = math.ceil(len(markets) / divisor)

        for channel in self.channels:
            if len(markets) <= max_subscriptions:
                self.ubwa.create_stream(channel, markets, stream_label=channel)
            else:
                loops = 1
                i = 1
                markets_sub = []
                for market in markets:
                    markets_sub.append(market)
                    if i == max_subscriptions or loops*max_subscriptions + i == len(markets):
                        self.ubwa.create_stream(channel, markets_sub, stream_label=str(channel+"_"+str(i)),
                                        ping_interval=10, ping_timeout=10, close_timeout=5)
                        markets_sub = []
                        i = 1
                        loops += 1
                    i += 1
        return True
    
    def print_stream_data_from_stream_buffer(self, binance_websocket_api_manager):
        while True:
            if binance_websocket_api_manager.is_manager_stopping():
                exit(0)
            oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
            if oldest_stream_data_from_stream_buffer is not False:
                unicorn_fied_stream_data = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
                try:
                    kline = unicorn_fied_stream_data['kline']
                except:
                    continue
                ourChannel = ['1d', '4h', '1h', '30m', '15m', '5m', '1m']
                if kline['interval'] in ourChannel:
                    symbol = unicorn_fied_stream_data['symbol'].upper()
                    kline = {x: kline[x] for x in kline if x == "symbol" or x == "interval" or x == "open_price" or x == "close_price" or x == "high_price" or x == "low_price" or x == "base_volume" or x == "is_closed"}
                    self.SH.kline_control(kline)
            else:
                time.sleep(0.01)