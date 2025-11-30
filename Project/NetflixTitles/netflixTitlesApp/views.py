from django.shortcuts import render
from netflixTitlesApp.models import NetflixTitles
from .search import filterTitles
from .graphs import createSubplots
import matplotlib.pyplot as plt
import pandas as pd

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


def year_view(request):
    years = (
        NetflixTitles.objects
        .values_list("release_year", flat=True)
        .distinct()
        .order_by("release_year")
    )

    genre_values = (
        NetflixTitles.objects
        .values_list("listed_in", flat=True)
        .distinct()
        .order_by("listed_in")
    )

    genre = set()

    for item in genre_values:
        for g in item.split(","):
            genre.add(g.strip())
    genres = sorted(genre)

    country_values = (
        NetflixTitles.objects
        .values_list("country", flat=True)
        .distinct()
        .order_by("country")
    )

    country = set()
    for item in country_values:
        if item and item.lower() != "nan":
            for c in item.split(","):
                cleaned = c.strip()
                if cleaned and cleaned.lower() != "nan":
                    country.add(cleaned)
    country = sorted(country)

    title = request.GET.get("title")
    director = request.GET.get("director")
    cast = request.GET.get("cast")
    year = request.GET.get("release_year")

    selectedGenres = request.GET.getlist("genres")
    selectedCountries = request.GET.getlist("countries")

    results = filterTitles(
        title=title,
        director=director,
        cast=cast,
        year=year,
        selectedGenres=selectedGenres,
        selectedCountries=selectedCountries
    )

    return render(request, "Homepage.html", {"years": years, "genre": genres, "country":country, "results": results})

def graphs(request):
    fig, axs = plt.subplots(3,1, figsize=(10,8))

    axs[0].barh(df_catagory_count_names, df_catagory_count_numbers, color='g')
    axs[0].set_title("Top 5 most popular genres on Netflix")

    axs[1].bar(df_country_count_names, df_country_count_numbers, color='b')
    axs[1].set_title("Top 5 countries with the most Netflix titles")

    axs[2].pie(df_rating_count_numbers, labels=df_rating_count_names)
    axs[2].set_title("Content Rating distribution")

    plt.tight_layout()
    plt.show()

    return render(request, "graphs.html",)