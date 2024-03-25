import requests
import os
import click 
import json

API_KEY = os.environ["GIPHY_API_KEY"]



class GiphyAPI:
	def __init__(self, api_key):
		self.key = api_key
	def get_trending(self, count):	
		if count is None or count > 25 or count < 1:
			count = 1
		result = requests.get("https://api.giphy.com/v1/gifs/trending?api_key="+self.key+"&limit=" + str(count) +"&offset=0&rating=g")
		return result.json()
	def get_search(self, count, q):
		if count is None or count > 25 or count < 1:
			count = 1
		result = requests.get("https://api.giphy.com/v1/gifs/search?api_key="+self.key+"&q=" + q + "&limit=" + str(count) +"&offset=0&rating=g")
		return result.json()

class GiphyCLI:
	def __init__(self):
		self.api = GiphyAPI(API_KEY)
	def construct_trending(self, count, md):
		data = self.api.get_trending(count)
		#data = json.dumps(data["data"], sort_keys=True, indent=4)
		#print(json.dumps(data["data"][1], sort_keys=True, indent=4))
		#print(data["data"][0]["bitly_url"])
		constructed = ''

		if count < 1:
			return "Please request at least 1 result."

		if not md:
			for n in range(count):
				constructed = constructed + str(n+1) + ") " + data["data"][n]["title"] + " " + data["data"][n]["bitly_url"] + "\n"
		else: #lol
			for n in range(count):
				constructed = constructed + str(n+1) + ") ![" + data["data"][n]["title"] + "](" + data["data"][n]["bitly_url"] + ")\n"

		return constructed
	def construct_search(self, count, md, term, lucky):
		data = self.api.get_search(count, term)

		return "..."
	def print_trending(self, count, md):
		print(self.construct_trending(count, md))
	def print_search(self, count, md, term, lucky):
		print(self.construct_search(count, md, term, lucky))

cli = GiphyCLI()

@click.group() 
def gif():
    print("hello from giphy cli!")
    APITests()
    CLITests()


@gif.command()
@click.option('--markdown', is_flag=True, default=False) 
@click.option('--count', default=5)
def trending(count, markdown):
    print("trending subcommand called!")
    cli.print_trending(count, markdown)
    #api = GiphyAPI(API_KEY)
    #print(api.get_trending(int(count)))

@gif.command()
@click.option('--lucky', is_flag=True, default=False)
@click.option('--markdown', is_flag=True, default=False)
@click.option('--count', default=5)
@click.argument("term")
def search(count, markdown, lucky, term):
    print("search subcommand called!")
    cli.print_search(count, markdown, lucky, term)

def CLITests(): 
	trending = cli.construct_trending(5, False)
	if len(trending) <= len("https://giphy.com/"): #our message will at least be this long
		print("CLI TEST FAILED, did not return a constructed trending list")
		print("ABORTING CLI TESTS!")
		return
	trending = cli.construct_trending(0, False)
	if trending != "Please request at least 1 result.":
		print("CLI TEST FAILED, did not return warning when trending count set to 0")
	trending = cli.construct_trending(5, True)
	if len(trending) >= 4 and trending[3] != "!":
		print("CLI TEST FAILED, did not print trending in markdown when asked")

	search = cli.construct_search(5, False, "cat", False)
	if len(search) <= len("https://giphy.com/"): #our message will at least be this long
		print("CLI TEST FAILED, did not return a constructed search list")
		print("ABORTING CLI TESTS!")
		return
	search = cli.construct_search(0, False, "cat", False)
	if search != "Please request at least 1 result.":
		print("CLI TEST FAILED, did not return warning when search count set to 0")
	search = cli.construct_search(5, True, "cat", False)
	if len(search) >= 4 and search[3] != "!":
		print("CLI TEST FAILED, did not print search in markdown when asked")
	
	search = cli.construct_search(5, True, "cat", True)
	if search[len(search)-1] != '\n':
		print("CLI TEST FAILED, did not print a single result when \'feeling lucky\'")

def APITests():
	api = GiphyAPI(API_KEY)
	resp = api.get_trending(5)

	if resp["meta"]["status"] == 401:
		print("API TEST FAILED, API KEY INCORRECT")
		print("ABORTING API TESTS!")
		exit()
		return

	try:
		if resp["pagination"]["total_count"] < 5:
			print("API TEST FAILED, TRENDING DID NOT RETURN AT LEAST 5 RESULTS")
	except: # hahahaha
		print()

	resp = api.get_search(5, "cat")

	if resp["meta"]["status"] != 200:
		print("API TEST FAILED, STATUS RETURNED FROM SEARCH NOT 200/OK")

if __name__ == "__main__":
	gif()
