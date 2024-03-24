import requests
import os

API_KEY = os.environ["GIPHY_API_KEY"]

def main():
    print("hello world")
    result = requests.get("https://api.giphy.com/v1/gifs/trending?api_key="+API_KEY+"&limit=25&offset=0&rating=g")
    print(result.text)


if __name__ == "__main__":
    main()
