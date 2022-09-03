import time
import datetime
import pandas as pd
import ta
from binance import Client
import os
import csv

class data():
	def __init__(self,symbol) :
		self.symbol = symbol
	def data(symbol, interval ,lookback,client) :
		def getdata(symbol,interval,lookback,client) :

			frame = pd.DataFrame(client.get_historical_klines(
				symbol,
				interval,
				lookback +'hour ago UTC'))
			frame = frame.iloc[:,:6]
			frame.columns =['Time', 'Open', 'High', 'Low', 'Close','Volume']
			frame= frame.set_index('Time')
			frame = frame.astype(float)
			return frame
		def applydata(df) :
			df['K'] = ta.momentum.stoch(df.High,df.Low,df.Close, window =14, smooth_window=3)
			df ['D']= df['K'].rolling(3).mean()
			df['rsi'] = ta.momentum.rsi(df.Close, window=6)
			df['macd'] = ta.trend.macd_diff(df.Close)
			df.dropna(inplace = True)
		frame = getdata(symbol, interval ,lookback,client)
		applydata(frame)
		return frame
class w_order():
	def __init__(self, symbol):
		self.symbol = symbol
	def login(self,API_KEY,API_SECRET) :
		client = Client (API_KEY, API_SECRET)
		int(time.time() * 1000) - client.get_server_time()['serverTime']
		time.sleep(2)
		print("Log in : Success")
		return client
	def wdata(self,order,rate,statuss) :
		log_dir_path='D:\log_coin'
		os.makedirs(log_dir_path,exist_ok=True)
		d = datetime.datetime.now()
		timestr=d.strftime('%Y%m%d') 
		logfile_name= ('BOT'+"_"+timestr+'.csv') 
		with open(os.path.join(log_dir_path,logfile_name),'a+',newline = '') as f :
			keys = ['orderId', 'symbol', 'rate', 'status','side','type']
			writer = csv.DictWriter(f,fieldnames = keys)
			writer.writerow({'orderId':str(order['orderId']),
				'symbol':str(order['symbol']),
				'rate' :str(rate),
				'status' : str(order['status']),
				'side' : str(order['side']),
				'type' : str(statuss)
				})
		print('Writed Data in File CSV')

	def check_csv(self,client) :
			print("Checking CSV : Loading.....")
			def check():
				try :
					log_dir_path='D:\log_coin' 
					os.makedirs(log_dir_path,exist_ok=True)
					d = datetime.datetime.now()
					timestr=d.strftime('%Y%m%d') 
					logfile_name= ('\BOT'+"_"+timestr+'.csv') 
					data = pd.read_csv(log_dir_path+logfile_name)
				except :
					print('Good Luck for new today')
					log_dir_path='D:\log_coin' 
					os.makedirs(log_dir_path,exist_ok=True)
					d = datetime.datetime.now()
					timestr=d.strftime('%Y%m%d') 
					logfile_name= ('BOT'+"_"+timestr+'.csv') 
					with open(os.path.join(log_dir_path,logfile_name),'a+') as f :
						keys = ['orderId', 'symbol', 'rate', 'status','side','type']
						writer = csv.DictWriter(f, fieldnames=keys)
						writer.writeheader()
						result = "Creat File CSV"
						print(result)
			def wait() :
				check()
				orders = client.get_all_orders(symbol='BTCBUSD')
				order = orders[len(orders) - 1]
				if order['side'] == 'BUY':
					if order['status'] == 'CANCELED' or order['status'] == 'FILLED':
						symbol = order['symbol'].rstrip('BUSD')
						balance = float(client.get_asset_balance(asset=symbol)['free'])
						if balance > 0:
							result = False
						else:
							result = True
					elif order['status'] == 'NEW' :
						result = False

				elif order['side'] =='SELL' :

					if order['status'] == 'CANCELED' or order['status'] == 'FILLED':
						symbol = order['symbol'].rstrip('BUSD')
						balance = float(client.get_asset_balance(asset=symbol)['free'])
						if balance > 0:
							result = False
						else:
							result = True
					elif order['status'] == 'NEW':
						result = False

				else :
					checkcsv = 'File empty'
					print(checkcsv)
					qty = float(client.get_asset_balance(asset='BTC')['free'])
					if qty > 0:
						result = False
					else:
						result = True
				return result
			return wait()
	def check_value(self,client):
		symbol = self.symbol
		rate = False
		while not rate :
			value = float(client.get_asset_balance(asset='BUSD')['free'])
			qty = float(client.get_asset_balance(asset=symbol.rstrip("BUSD"))['free'])
			df = data.data(symbol, '15m' ,'30',client)
			price_current = df.Close.iloc[-1]
			balance = qty * price_current
			if value >= 11 :
				print("		Ready Value : True")
				qty = value/price_current
				qty = round(qty - (1 / price_current), 5)
				rate = True
				print('Trade :', symbol, qty)
				return rate,qty,value
			elif balance > 10 :
				print("		Ready Value : True")
				print('Trade :', symbol, qty)
				rate = True
				return  rate,qty,value
			else :
				time.sleep(5)
				rate = False
