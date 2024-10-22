import requests
import pandas as pd
import plotly.graph_objects as go

class Stockfetch:

    def __init__(self,api_key):
        self.api_key = api_key
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"
        }
    
    def symbol_search(self,company):
        querystring = {
            "datatype": "json",
            "keywords": company,
            "function": "SYMBOL_SEARCH",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()["bestMatches"]
        dct = {}
        for i in data:
            symbol = i["1. symbol"]
            dct[symbol] = [i["2. name"], i["3. type"], i["4. region"]]
        return dct
    
    def daily_data(self, symbol):
        querystring = {
            "function": "TIME_SERIES_DAILY",
            "symbol":symbol,
            "outputsize":"compact",
            "datatype":"json"
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        df = pd.DataFrame(response.json()["Time Series (Daily)"]).T
        df.index = pd.to_datetime(df.index)
        for i in df.columns:
            df[i] = df[i].astype(float)
        return df
    
    def plot_chart(self, symbol):
        df = self.daily_data(symbol)
        fig = go.Figure(data=[
            go.Candlestick(
            x = df.index,
            open = df["1. open"],
            high = df["2. high"],
            low = df["3. low"],
            close = df["4. close"]
            )
        ])
        fig.update_layout(width=1000, height=800)
        return fig
