from application import app
from flask import render_template, url_for
from application.fetcher import PlaceToLive
from requests_html import HTMLSession

import pandas as pd
import json
import plotly
import plotly.express as px
import datetime

@app.route("/")
def index():
    # url = 'https://www.airbnb.com/rooms/52553164'
    # session = HTMLSession()
    # currAirBnB = PlaceToLive(url, session)
    # currAirBnB.getAllInfo()

    begin_date = datetime.date(2022, 2, 4)
    one_day = datetime.timedelta(days=1)
    d = {'Date': [begin_date, begin_date+one_day, begin_date+one_day+one_day], 'Price': [3, 4,7]}
    df = pd.DataFrame(data=d)
    fig1 = px.line(df, x='Date', y='Price', title = "Price Curve")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", graph1JSON = graph1JSON)