import requests
import os
import click 

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
	def __init(self):
		self.api = GiphyAPI(API_KEY)
	def construct_trending(self, count, md):
		return "..."
	def construct_search(self, count, md, term):
		return "..."
	def print_trending(self, count, md):
		print(self.construct_trending(count, md))
	def print_search(self, count, md, term):
		print(self.construct_search(count, md, term))

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
@click.option('--markdown', is_flag=True, default=False)
@click.option('--count', default=5)
@click.argument("term")
def search(count, markdown, term):
    print("search subcommand called!")
    cli.print_search(count, markdown, term)

def CLITests(): 
	trending = cli.construct_trending(5, False)
	if len(trending) <= len("https://giphy.com/"): #our message will at least be this long
		print("CLI TEST FAILED, did not return a constructed list")
		print("ABORTING CLI TESTS!")
		return
	trending = cli.construct_trending(0, False)
	if trending != "Please request at least 1 result.":
		print("CLI TEST FAILED, did not return warning when count set to 0")
	trending = cli.construct_trending(5, True)
	if len(trending) >= 4 and trending[3] != "!":
		print("CLI TEST FAILED, did not print in markdown when asked")

def APITests():
	api = GiphyAPI(API_KEY)
	resp = api.get_trending(5)

	if resp["meta"]["status"] == 401:
		print("API TEST FAILED, API KEY INCORRECT")
		print("ABORTING API TESTS!")
		exit()
		return

	if resp["pagination"]["total_count"] < 5:
		print("API TEST FAILED, TRENDING DID NOT RETURN AT LEAST 5 RESULTS")

	resp = api.get_search(5, "cat")

	if resp["meta"]["status"] != 200:
		print("API TEST FAILED, STATUS RETURNED FROM SEARCH NOT 200/OK")

if __name__ == "__main__":
    gif()
