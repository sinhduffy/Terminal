import time
import datetime
import pandas as pd
import os
import strategy
from worder import data
import scratch as AI
class count :
	def count_down_15m(self):
		d = datetime.datetime.now()
		time_m = int(d.strftime("%M"))
		time_s = int(d.strftime("%S"))
		time_count = time_m*60 + time_s
		time.sleep(1)
		timelist = [15*60,30*60,45*60,60*60]
		for i in timelist :
			if i - time_count > 0 :
				time_sec = i - time_count
				break
		while time_sec:
			#df = data.data(self.pair, '15m' ,'30',client)
			#price_current = df.Close.iloc[-1]
			mins, secs = divmod(time_sec, 60)
			timeformat = '{:02d}:{:02d}'.format(mins, secs)
			print('Waiting : ',timeformat, end='\r')
			time.sleep(1)
			time_sec -= 1
	def count_down_1m(self):
		d = datetime.datetime.now()
		time_m = int(d.strftime("%M"))
		time_s = int(d.strftime("%S"))
		time_count = time_m*60 + time_s
		time.sleep(1)
		timelist = [1*60]
		for i in timelist :
			if i - time_count > 0 :
				time_sec = i - time_count
				break
		while time_sec:
			#df = data.data(self.pair, '15m' ,'30',client)
			#price_current = df.Close.iloc[-1]
			mins, secs = divmod(time_sec, 60)
			timeformat = '{:02d}:{:02d}'.format(mins, secs)
			print('Waiting : ',timeformat, end='\r')
			time.sleep(1)
			time_sec -= 1
class tradingcoin :
	def __init__(self, symbol,client):
		self.symbol = symbol
		self.client = client
	def buy_coin(self,qty,price_buy) :
		symbol = self.symbol
		client = self.client
		order = client.order_limit_buy(
		symbol = symbol,
		quantity= qty,
		price= price_buy)
		return order
	def sell_coin(self,qty,price_sell) :
		symbol = self.symbol
		client = self.client
		order = client.order_limit_sell(
		symbol = symbol,
		quantity = qty,
		price = price_sell)
		return order
	def strategybuy(self) :
		is_area = False
		def checkcoin(symbol,client) :
			Close = []
			RSI = []
			Amp = []
			df = strategy.data.data(symbol, '15m', '30', client)
			rsi6 = round(df.rsi.iloc[-1], 2)
			price_current = df.Close.iloc[-1]
			if price_current > 10000:
				n = -1
			elif price_current > 1000:
				n = 1
			else:
				n = 2
			# Created High and Low
			for i in range(0, 86):
				a = round(df.Close.iloc[i], n)
				Close.append(a)
			Close.sort()
			print("L:", Close[0], "H", Close[-1])
			x = 0
			for i in Close:
				if Close.count(i) > x:
					x = Close.count(i)
					offer_price = i
			# Creatd Amplidute

			for i in range(0, 86):
				L = round(df.Low.iloc[i], 3)
				H = round(df.High.iloc[i], 3)
				amp = (H - L) / L * 100
				Amp.append(amp)
			Amp.sort()
			amp_average = round(sum(Amp) / len(Amp), 2)
			if offer_price > df.Close.iloc[-1]:
				print('Price Current : ', df.Close.iloc[-1], ' | ', 'Price Hinder : ', offer_price, 'Amp_average :',
					  amp_average);
				a = False
			else:
				print('Price Current : ', df.Close.iloc[-1], 'Price Support : ', offer_price, 'Amp_average :',
					  amp_average); a = True
			for i in range(0, 86):
				b = df.rsi.iloc[i]
				RSI.append(b)
			rsi = round((sum(RSI) / (len(RSI) - 1)) / 1.618, 2) # + rsi_trade
			print("RSI Trade :", rsi, "RSI Current : ", rsi6)
			return  Close,rsi,offer_price,a,amp_average
		def AI_BUY(is_area,Close,rsi,offer_price,a,amp_average,symbol,client) :
			global buy
			symbol = self.symbol
			client = self.client
			df = data.data(symbol, '15m', '30', client)
			rsi6 = round(df.rsi.iloc[-1], 2)
			price_current = df.Close.iloc[-1]
			volume = df.Volume.iloc[-1]
			d = datetime.datetime.now()
			timestr = d.strftime('%H:%M:%S')
			# Check_Tools
			check_low = Close[0] - Close[0] * 0.0012
			check_of_min = round(offer_price * 1.0002, 2)
			check_of_max = 0.9998 * offer_price
			#		check_new_bullish = Close[-1]*1.01
			check_offer = round(Close[0] * 1.007, 2)
			check_rsi = 0.5 * rsi
			rsi_check = rsi6 > check_rsi
			check_buy_break = price_current >= 1.0087 * Close[-1]
			check_change_offer = round(offer_price * (1 + amp_average / 50), 2)
			check_area_trade_min = round(Close[0] * (amp_average * 0.02 + 1), 2)
			check_area_trade_max = round(Close[-1] * (1 - amp_average * 0.006), 2)
			check_area_trade = check_area_trade_max - check_area_trade_min
			check_Close = round(df.Close.iloc[85], -1) + round(df.Close.iloc[84], -1) + round(df.Close.iloc[83],-1) / 3 == round(df.Close.iloc[83], -1)
			price_open = df.Open.iloc[85]
			price_close = df.Close.iloc[85]
			rate_cot = str((price_open - price_close) / price_open * 100)
			rate_cot = float(rate_cot[0:5])

			if check_buy_break :
				status = 'check_buy_break'
				print('Buy', status, timestr)
				ifbuy = True
				buy = True
			# Buy support price
			elif price_current <= check_of_min and price_current >= check_of_max and a and price_current >= check_offer:
				status = 'offer_price'
				print('Buy:',status, timestr)
				ifbuy = True
				buy = True
			# Buy Lowest price in zone trade
			elif price_current < check_low and rsi6 >= check_rsi :
				status = 'lower'
				print('Buy', status, timestr)
				print("BUY Lower : ", price_current, 'Time :', timestr)
				ifbuy = True
				buy = True
			# Buy follow RSI
			elif rsi6 <= rsi and rsi_check :
				status = 'RSI'
				print('Buy', status, timestr)
				ifbuy = True
				buy = True
			# Change Offer when overriding the old Offer
			# Creating zone looptrade

			elif (check_low - 50 > price_current) :
				print()
				print('Out of range : Resset ', 'Time :', timestr)
				ifbuy = True
				count.count_down_15m()
			# To avoid catching falling knives
			elif check_Close:
				status = 'check_CLose'
				print('Buy', status, timestr)
				ifbuy = True
				buy = True
			elif rate_cot == -0.12:
				status = 'rate_cot'
				print('Buy', status, timestr)
				ifbuy = True
				buy = True

			else :
				ifbuy = False
				buy = False
				rsi_check = False
				offer_check = False
				is_area = False
				status = 'None'
				time.sleep(0.25)
				print("|", price_current, "|",
					  volume,"|",
					  rsi_check, check_low, "|",
					  check_of_min, offer_check, "|",
					  "SwichZone ", check_area_trade_min, check_area_trade_max,
					  end='\r')
			return ifbuy, buy, price_current, is_area, status
		symbol = self.symbol
		client = self.client
		print(' Waiting for Opportunities to BUY ')
		log_dir_path = 'D:\log_coin\pestbot'
		os.makedirs(log_dir_path, exist_ok=True)
		logfile_name = ('\BOT.csv')
		datas = pd.read_csv(log_dir_path + logfile_name)
		price_sell_old = datas.price_sell.iloc[-1]
		ifbuy = False; buy = False
		is_area = False
		while not buy :
			Close, rsi, offer_price, a, amp_average = checkcoin(symbol, client)
			while not ifbuy :
				ifbuy, buy, price_current, is_area, status = AI_BUY(is_area, Close, rsi, offer_price, a, amp_average, symbol,
																	client)
		return buy, price_current, is_area, status
	def strategysell(self,status,price_buy) :
		def AI_SELL() :
			d = datetime.datetime.now()
			timestr = d.strftime('%H:%M:%S')
			if status == 'check_buy_break' :
				price_sell = AI.check_buy_beak(price_buy)
				ifsell = True
			elif status == 'lower' :
				price_sell = AI.check_buy_low(price_buy)
				ifsell = True
			elif status == 'RSI' :
				price_sell = AI.check_RSI(price_buy)
				ifsell = True
			elif status == 'check_CLose' :
				price_sell = AI.check_Close(price_buy)
				ifsell = True
			elif status == 'rate_cot' :
				price_sell = AI.check_rate_cot(price_buy)
				ifsell = True
			elif status == 'is_area' :
				price_sell = AI.is_erea(price_buy)
				ifsell = True
			else :
				ifsell = False
				price_sell = NameError
			print("Price_Buy :", price_buy, status, price_sell)
			return ifsell,price_sell
		def AI_LOOP():
			def SELL():
				while True:
					d = datetime.datetime.now()
					timestr = d.strftime('%H:%M:%S')
					df = data.data(symbol, '15m', '30', client)
					price_current = df.Close.iloc[-1]
					check_stoploss_min = price_current + 30
					price_stoploss_min = check_stoploss_min - 5
					time.sleep(0.5)
					print(price_current, check_stoploss_min, end='\r')

					# print('Price_Current :',price_current ,'Price_Stoploss :',round(price_stoploss*0.998,n),end ='\r')
					if  price_current >= price_stoploss_min:
						print()
						print('Target : ', price_current, 'Time :', timestr)
						break
					elif price_current > check_stoploss_min:
						price_stoploss = price_current
						print()
						print('Change Stoploss : ', price_stoploss,
							  'Time :', timestr)
				return price_current
			price_sell = SELL()
			ifsell = True
			return ifsell, price_sell

		symbol = self.symbol
		client = self.client
		ifsell = False

		print('Waiting for Opportunities to SELL')
		target = 1.0025
		stoploss = round(price_buy * 0.995, 3)
		offer_price_sell = round(price_buy*target,2)
		if status == 'None' :
			while not ifsell:
				ifsell,price_sell = AI_LOOP()
		else :
				ifsell, price_sell = AI_SELL()
		return ifsell,price_sell