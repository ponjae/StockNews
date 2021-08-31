import requests
import smtplib
from credentials import my_credentials

news_key = my_credentials["news_key"]
stock_key = my_credentials["stock_key"]
email = my_credentials["email"]
password = my_credentials["password"]

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_key
}

news_params = {
    "q": COMPANY_NAME,
    "apiKey": news_key
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (_, value) in stock_data.items()]
close_yesterday = float(stock_data_list[0]["4. close"])
close_day_before_yesterday = float(stock_data_list[1]["4. close"])

difference = close_yesterday - close_day_before_yesterday
if difference > 0:
    up_down = "Up:"
else:
    up_down = "Down:"

percentage = abs(difference) / close_yesterday

if percentage >= 0.0005:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]

    print(news_data)

    formatted_articles = [
        f"Headline: {article['title']}. \nBrief: {article['description']}" for article in news_data]

    for article in formatted_articles:
        print(50 * '*')
        print(article)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        for article in formatted_articles:
            connection.sendmail(from_addr=email,
                                to_addrs="ponjae11@gmail.com", msg=f"Subject:Tesla {up_down} {round(percentage * 100)}%\n\n" + article)
