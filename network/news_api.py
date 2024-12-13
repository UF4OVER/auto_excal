import requests

def get_news(limit=1):
    url = f'https://api.thenewsapi.com/v1/news/top?api_token=kMhHXojE5ApSocUeSmpMGZblAi9g8gkkfmPd2FoT&locale=cn&limit={limit}'
    response = requests.get(url)

    return response.json()


def refresh_news():
    pass



if __name__ == "__main__":
    a = get_news()
    print(a["data"][0]["title"])
    print(a["data"][0]["description"])
    print(a["data"][0]["image_url"])
