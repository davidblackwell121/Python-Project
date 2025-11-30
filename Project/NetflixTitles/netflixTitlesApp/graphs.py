from django.db import models
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64


def createSubplots():
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

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    genre_colors = ['red', 'green', 'blue', 'orange', 'purple']
    axs[0].barh(df_catagory_count_names, df_catagory_count_numbers, color=genre_colors)
    axs[0].invert_yaxis()
    axs[0].set_title("Top 5 Most Popular Genres on Netflix", fontweight='bold')
    axs[0].set_xlabel("Number of Titles", fontweight='bold')

    country_colors = ['red', 'green', 'blue', 'orange', 'purple']
    axs[1].bar(df_country_count_names, df_country_count_numbers, color=country_colors)
    axs[1].set_title("Top 5 Countries with the Most Netflix Titles", fontweight='bold')
    axs[1].tick_params(axis='x')
    axs[1].set_ylabel("Number of Titles", fontweight='bold')

    rating_counts = pd.Series(df_rating_count_numbers, index=df_rating_count_names)
    small = rating_counts[rating_counts / rating_counts.sum() < 0.05]
    large = rating_counts[rating_counts / rating_counts.sum() >= 0.05]
    if not small.empty:
        large['Other'] = small.sum()

    rating_colors = ['cyan', 'magenta', 'yellow', 'lime', 'brown', 'pink']
    axs[2].pie(
        large,
        labels=large.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=rating_colors
    )
    axs[2].set_title("Content Rating Distribution", fontweight='bold')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4) # Adds some horizontal spacing between each graph

    # Saves figure to a PNG in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode PNG to base64 string to embed in HTML
    graph_base64 = base64.b64encode(image_png).decode('utf-8')
    return graph_base64
