from flask import Flask, render_template, request
from flask_table import Table, Col
import pandas as pd
import os
from getrec import get_recommendations

app = Flask(__name__)

#Input page Page
@app.route('/')
def home():
    return render_template("index.html")

#result page
@app.route("/recommendation", methods = ["GET", "POST"])
def recommendation():
    if request.method == "POST":
        try:
            title = request.form["title"].strip() #reading the dataset
            df = pd.read_csv("Openrice_Transformed_V4.csv", low_memory=False)
            df_10 = get_recommendations(title, df)
            restName, restLink, dist, ratAvg, waitAvg = (list(df_10[i]) for i in df_10.columns)
            return render_template("recommendation.html", name=restName, link=restLink, district=dist, rating=ratAvg, wait=waitAvg)
        except:
            return render_template("failure.html")

@app.route("/restaurants")
def load_restaurants():
    df = pd.read_csv("Openrice_Transformed_V4.csv", low_memory=False)
    cli_df = df.sort_values('Cuisine')[['Restaurant_Name','District','Cuisine']]
    cli_rest, cli_dis, cli_cui = (list(cli_df[col])for col in cli_df.columns)
    len_rest = len(cli_rest) #number of listed restaurants
    return render_template("restaurants.html", rname=cli_rest, rdist=cli_dis, rcui=cli_cui, rlen=len_rest)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
