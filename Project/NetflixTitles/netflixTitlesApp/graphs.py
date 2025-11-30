from django.db import models
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv('netflixTitlesApp/netflix_titles.csv')

filled_df = df.fillna("No info Available")

genre_series = filled_df['listed_in'].str.split(',').explode().str.strip()

df_genre_count = genre_series.value_counts().head(5)

df_catagory_count_names = df_genre_count.index.tolist()

df_catagory_count_numbers = df_genre_count.values.tolist()

df_country_count = df['country'].value_counts().head(5)

df_country_count_names = df_country_count.index.tolist()

df_country_count_numbers = df_country_count.values.tolist()

df_rating_count = df['rating'].value_counts()

df_rating_count_names = df_rating_count.index.tolist()

df_rating_count_numbers = df_rating_count.values.tolist()


def createSubplots():
    
    genreBar = plt.barh(df_catagory_count_names, df_catagory_count_numbers, color='g')
    genreBar.set_title("Top 5 most popular genres on Netflix")

    countryBar= plt.bar(df_country_count_names, df_country_count_numbers, color='b')
    countryBar.set_title("Top 5 countries with the most Netflix titles")

    contentPie = plt.pie(df_rating_count_numbers, labels=df_rating_count_names)
    contentPie.set_title("Content Rating distribution")

    return (genreBar,countryBar,contentPie)
