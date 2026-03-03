from credentials import Credential
import requests
from twilio.rest import Client

# Stock API
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = Credential.stock_api_key
STOCK_ENDPOINT = Credential.stock_endpoint

# News API
NEWS_API_KEY = Credential.news_api_key
NEWS_ENDPOINT = Credential.news_endpoint

# Twilio
account_sid = Credential.twilio_sid
auth_token = Credential.twilio_auth_token

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "5min",
    "apikey": STOCK_API_KEY,
}
stock_res = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_res.raise_for_status()
stock_data = stock_res.json()["Time Series (Daily)"]

stock_price_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_price_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

two_days_ago_data = stock_price_list[1]
two_days_ago_closing_price = float(two_days_ago_data["4. close"])

price_diff = yesterday_closing_price - two_days_ago_closing_price

up_down = None
if price_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage = round((price_diff / yesterday_closing_price), 2) * 100

if abs(percentage) >= 3:
    news_params = {
        "q": COMPANY_NAME,
        "language": "en",
        "apiKey": NEWS_API_KEY,
    }

    news_res = requests.get(NEWS_ENDPOINT, news_params)
    news_res.raise_for_status()
    news_articles = news_res.json()["articles"]

    three_articles_list = news_articles[0:3]

    articles_summary = [f"Headline: {article['title']} \nBrief: {article['description']}" for article in three_articles_list]

    client = Client(account_sid, auth_token)
    for article in articles_summary:
        message = client.messages.create(
            from_="whatsapp:+14155238886",
            body=f"{STOCK_NAME}: {up_down} {percentage}%\n"
                 f"{article}",
            to="whatsapp:+18572588770"
        )
        print(message.body)
        print(message.status)