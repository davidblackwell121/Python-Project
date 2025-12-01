from django.shortcuts import render
from netflixTitlesApp.models import NetflixTitles
from .search import filterTitles
from .graphs import createSubplots
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('netflixTitlesApp/netflix_titles.csv') # Reads the dataset
filled_df = df.fillna("No info Available") # Replaces and missing values with a placeholder

# Count top 5 genres
genre_series = filled_df['listed_in'].str.split(',').explode().str.strip()
df_genre_count = genre_series.value_counts().head(5)
df_catagory_count_names = df_genre_count.index.tolist()
df_catagory_count_numbers = df_genre_count.values.tolist()

# Count top 5 countries
df_country_count = df['country'].value_counts().head(5)
df_country_count_names = df_country_count.index.tolist()
df_country_count_numbers = df_country_count.values.tolist()

# Count title ratings
df_rating_count = df['rating'].value_counts()
df_rating_count_names = df_rating_count.index.tolist()
df_rating_count_numbers = df_rating_count.values.tolist()

def year_view(request):
    # Grabs unique release years from the database
    years = (
        NetflixTitles.objects
        .values_list("release_year", flat=True)
        .distinct()
        .order_by("release_year")
    )

    # Gets unique genre strings ('horror' 'action' etc.) from the database
    genre_values = (
        NetflixTitles.objects
        .values_list("listed_in", flat=True)
        .distinct()
        .order_by("listed_in")
    )

    # Splits the genre strings into individual names
    genre = set()
    for item in genre_values:
        for g in item.split(","):
            genre.add(g.strip())
    genres = sorted(genre)

    # Gets unique country values
    country_values = (
        NetflixTitles.objects
        .values_list("country", flat=True)
        .distinct()
        .order_by("country")
    )

    # Used to grab and sort all the countries while removing invalid entries such as 'NaN'
    country = set()
    for item in country_values:
        # Skip blank and on-valid entries
        if item and item.lower() != "nan":
            for c in item.split(","):
                cleaned = c.strip()
                if cleaned and cleaned.lower() != "nan":
                    country.add(cleaned)
    country = sorted(country)

    # Gets search parameters
    title = request.GET.get("title")
    director = request.GET.get("director")
    cast = request.GET.get("cast")
    year = request.GET.get("release_year")

    # Gets all checkbox options
    selectedGenres = request.GET.getlist("genres")
    selectedCountries = request.GET.getlist("countries")

    # Filters the titles based on the selected criteria
    results = filterTitles(
        title=title,
        director=director,
        cast=cast,
        year=year,
        selectedGenres=selectedGenres,
        selectedCountries=selectedCountries
    )

    # Re-render the homepage with the new results
    return render(request, "Homepage.html", {"years": years, "genre": genres, "country":country, "results": results})

# Called by graphs.html to render the graph images
def graphs(request):
    graph = createSubplots()
    return render(request, "graphs.html", {"graph": graph})