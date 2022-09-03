
import main_real as bot
from  binance import Client
class main :
	def __init__(self,symbol,client):
		self.symbol = symbol
		self.client = client
	def main(self) :
		symbol = self.symbol
		client = self.client
		ok = bot.run(symbol,client)

while True :
	while True :
		try:
			API_KEY = "fSeSCv293VEYU6k4l5dn0DzLIGJosCkQiPHXpMsvnJGw7XPZsjtYHb9fREyl2fEI"
			API_SECRET = "pwcGorfgOfY8Vp0LuE3WxEA6wRTGF7LixpzVpmXIoMoapcO1j93l7yfIobb5KtZP"
			client = Client(API_KEY,API_SECRET)
			symbol = 'BTCBUSD'
			runbot = main(symbol,client)
			runbot.main()
		except :
			print('DIE_NETWORK')
			bot.count(5*60)