import strategy as stg
import time
import datetime
import os
import csv
import pandas as pd
import ta
import winsound
import worder
def run(symbol,client) :

	print("#######----MODE----######".center(60))
	print('You at Trade_Mode'.center(60))
	defu = ['BTCBUSD','BNBBUSD','ETHBUSD']
	for de in defu :
		dtf = worder.data.data(de, '15m', '15', client)
		print(de,dtf.Close.iloc[-1])
	if symbol == "AVAX" :
		n = 2
	elif symbol == "BTC" :
		n = 5
	elif symbol == "ETH" :
		n = 2
	elif symbol == "ATOM" :
		n = 3
	elif symbol == "BNB" :
		n = 2
	else :
		n = 3
	print()
	ew = worder.w_order(symbol)
	strategy = stg.tradingcoin(symbol, client)
	rate,qty,value  = ew.check_value(client)

	while rate :
		check_order = ew.check_csv(client)
		if check_order :
			buy, price_buy, is_area, statuss = strategy.strategybuy()
			print('Check_order :', check_order)
			print(price_buy,qty,symbol)
			order = client.order_limit_buy(
						symbol = symbol,
						quantity= qty,
						price= price_buy)
			buy = False
			while not buy :
				orderId = order['orderId']
				status = "NEW"
				while status == 'NEW' :
					order = client.get_order(symbol=symbol,orderId= orderId)
					if order['status'] == 'FILLED' :
						print('Order matching : True')
						buy = True
						ew.wdata(order,rate,statuss)
					if order['status'] == "CANCELED" :
						print("Cancel Order : True")
					status = order['status']
			check_order = ew.check_csv(client)
		if not check_order :
			log_dir_path='D:\log_coin'
			os.makedirs(log_dir_path,exist_ok=True)
			d = datetime.datetime.now()
			timestr=d.strftime('%Y%m%d')
			logfile_name= ('\BOT'+"_"+timestr+'.csv')
			data = pd.read_csv(log_dir_path+logfile_name)
			if data.empty :
				timestr = str(int(timestr)-1)
				logfile_name = ('\BOT' + "_" + timestr + '.csv')
				data = pd.read_csv(log_dir_path + logfile_name)
				statuss = data.type.iloc[-1]
			else :
				statuss = data.type.iloc[-1]
			orders = client.get_all_orders(symbol='BTCBUSD')
			order = orders[len(orders) - 1]
			orderId = order['orderId']
			print('Get orderId : ', orderId)
			price_buy = float(order['price'])
			qty = float(order['origQty'])
			print()
			ifsell,price_sell = strategy.strategysell(statuss,price_buy)
			sell = False
			while not sell :
				order = strategy.sell_coin(qty,price_sell)
				orderId = order['orderId']
				status = "NEW"
				while status == 'NEW':
					order = client.get_order(
						symbol=symbol,
						orderId=orderId)
					if order['status'] == 'FILLED':
						print('Order matching : True')
						sell = True
						ew.wdata(order, rate, statuss)
						fees = client.get_trade_fee(symbol=symbol)['makerCommission']
						rate = (qty * (price_sell - price_buy) / value * 100) - float(fees)
					if order['status'] == "CANCELED":
						print("Cancel Order : True")
						sell = True
					status = order['status']
					count(5)


def count(time_sec):
	while time_sec:
		#df = data.data(self.symbol, '15m' ,'30',client)
		#price_current = df.Close.iloc[-1]
		mins, secs = divmod(time_sec, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		print('Waiting : ',timeformat, end='\r')
		time.sleep(1)
		time_sec -= 1
	return time_sec

def runtest(symbol,client):
	print("#######----MODE----######".center(120))
	print('You at TestMode'.center(120))
	def wq(symbol, interval ,lookback,client) :
		def getdata(symbol,interval,lookback,client) :

			frame = pd.DataFrame(client.get_historical_klines(
				symbol,
				interval,
				lookback +'hour ago UTC'))
			frame = frame.iloc[:,:6]
			frame.columns =['Timme', 'Open', 'High', 'Low', 'Close','Voloume']
			frame= frame.set_index('Timme')
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

	def wdata(order,rate) :
		log_dir_path='D:\log_coin\pestbot'
		os.makedirs(log_dir_path,exist_ok=True)
		d = datetime.datetime.now()
		timestr=d.strftime('%H%M%S')
		logfile_name= ('BOT.csv')
		with open(os.path.join(log_dir_path,logfile_name),'a+',newline = '') as f :
			keys = ['time','value','price_sell','rate']
			writer = csv.DictWriter(f,fieldnames = keys)
			f.write('\n\r')
			writer.writerow(
				{
				'time' :str(timestr),
				'value' : str(order['value']),
				'price_sell' : str(order['price_sell']),
				'rate' : str(rate)
				})

		print('Writed Data in File CSV')

	def check_csv(client) :
			print("Checking CSV : Loading.....")
			def check():
				try :
					log_dir_path='D:\log_coin\pestbot'
					os.makedirs(log_dir_path,exist_ok=True)
					logfile_name= ('\BOT.csv')
					data = pd.read_csv(log_dir_path+logfile_name)
				except :
					print('Good Luck for new today')
					log_dir_path='D:\log_coin\pestbot'
					os.makedirs(log_dir_path,exist_ok=True)
					logfile_name= ('BOT.csv')
					with open(os.path.join(log_dir_path,logfile_name),'a+') as f :
						keys = ['time','value']
						writer = csv.DictWriter(f, fieldnames=keys)
						writer.writeheader()
						result = "Creat File CSV"
						print(result)
			def wait() :
				check()
				log_dir_path='D:\log_coin\pestbot'
				os.makedirs(log_dir_path,exist_ok=True)
				d = datetime.datetime.now()
				timestr=d.strftime('%Y%m%d')
				logfile_name= ('\BOT.csv')
				data = pd.read_csv(log_dir_path+logfile_name)
				print(data)
				if data.empty :
					checkcsv = 'File empty'
					print(checkcsv)
					result = False
				else :
					checkcsv = 'Created File'
					print(checkcsv)
					df = wq(symbol, '15m' ,'30',client)
					price_current = df.Close.iloc[-1]
					result = True
					value = data.value.iloc[-1]
					qty = round(value/price_current,3) - 0.0002
				return result,value,qty
			return wait()

	print("#######----MODE----######".center(60))
	print('You at Trade_Mode'.center(60))
	defu = ['BTCBUSD','BNBBUSD','ETHBUSD']
	for de in defu :
		dtf = worder.data.data(de, '15m', '15', client)
		print(de,dtf.Close.iloc[-1])
	if symbol == "AVAX" :
		n = 2
	elif symbol == "BTC" :
		n = 5
	elif symbol == "ETH" :
		n = 2
	elif symbol == "ATOM" :
		n = 3
	elif symbol == "BNB" :
		n = 2
	else :
		n = 3
	print()
	ew = worder.w_order(symbol)
	dtf = worder.data.data(symbol,'15m','15',client)
	price = dtf.Close.iloc[-1]
	strategy = stg.tradingcoin(symbol, client)
	rate,value,qty  = check_csv(client)
	while True :
		check_order = ew.check_csv(client)
		if check_order :
			buy, price_buy, is_area, status = strategy.strategybuy()
			print('Check_order :', check_order)
			check_order = False
			winsound.Beep(600,500)
		if not check_order :
			ifsell,price_sell = strategy.strategysell(status,price_buy)
			rate = (qty * (price_sell - price_buy ) / value * 100)- 0.01
			rate = round(rate,2)
			d = datetime.datetime.now()
			timestr =d.strftime('%H:%M:%S')
			order = {
			'value' : round(value+rate*value/100,2),
			'time' : timestr,
			'price_sell' : price_sell,
			'rate' : rate
			}
			winsound.Beep(600,500)
		print(order)
		wdata(order,rate)
