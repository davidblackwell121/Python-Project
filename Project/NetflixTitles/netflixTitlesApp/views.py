from django.shortcuts import render
from netflixTitlesApp.models import NetflixTitles
from .search import filterTitles


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
        for c in item.split(","):
            country.add(c.strip())
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


def search(request):
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
    return render(request, "Homepage.html", {"results": results})