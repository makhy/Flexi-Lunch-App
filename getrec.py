import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def get_recommendations(title, df):
    tfidf = TfidfVectorizer(stop_words = "english")# load vector
    df["Reviews"] = df["Reviews"].fillna("") #replace nan with empty string
    tfidf_matrix = tfidf.fit_transform(df["Reviews"])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index = df["Restaurant_Name"])
    idx = indices[title] #get index of restuarant that matches the title
    sim_scores = list(enumerate(cosine_sim[idx])) #pairwise similarity scores of all restaurants
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) #sort scores
    sim_scores = sim_scores[1:11] #get scores of top 10 similar restaurants
    rest_indices = [i[0] for i in sim_scores] #Get the restaurant indices
    df_10 = df[["Restaurant_Name","Restaurant_Link","District","Rating_Average","Wait_Average"]].iloc[rest_indices]
    return df_10
