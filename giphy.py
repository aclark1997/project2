import requests
import os
import click

API_KEY = os.environ["GIPHY_API_KEY"]


class GiphyAPI:
	def __init__(self, api_key):
		self.key = api_key
	def get_trending(self, count):	
		if count is None or count > 25 or count < 1:
			count = 5
		result = requests.get("https://api.giphy.com/v1/gifs/trending?api_key="+self.key+"&limit=" + str(count) +"&offset=0&rating=g")
		return result.json()
	def get_search(self, count, q):
		if count is None or count > 25 or count < 1:
			count = 5
		result = requests.get("https://api.giphy.com/v1/gifs/search?api_key="+self.key+"&q=" + q + "&limit=" + str(count) +"&offset=0&rating=g")
		return result.json()

@click.group()
def gif():
    print("hello from giphy cli!")
    MediumTests()


@gif.command()
def trending():
    print("trending subcommand called!")
    api = GiphyAPI(API_KEY)


@gif.command()
def search():
    print("search subcommand called!")
    api = GiphyAPI(API_KEY)


def MediumTests():
	api = GiphyAPI(API_KEY)
	resp = api.get_trending(5)

	if resp["meta"]["status"] == 401:
		print("TEST FAILED, API KEY INCORRECT")
		print("ABORTING TESTS")
		exit()
		return

	if resp["pagination"]["total_count"] < 5:
		print("TEST FAILED, TRENDING DID NOT RETURN AT LEAST 5 RESULTS")

	resp = api.get_search(5, "cat")

	if resp["meta"]["status"] != 200:
		print("TEST FAILED, STATUS RETURNED FROM SEARCH NOT 200/OK")

if __name__ == "__main__":
    gif()
