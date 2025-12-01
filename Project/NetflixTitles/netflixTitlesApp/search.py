from .models import NetflixTitles
from django.db.models import Q


# Filters titles based on the below parameters
# Parameters are optional but each provided filter is added to the search
def filterTitles(
        title=None,
        director=None,
        cast=None,
        year=None,
        selectedGenres=None,
        selectedCountries=None
):
    # All titles from the dataset
    qs = NetflixTitles.objects.all()

    # Filters by title/director/cast/year/selected genre
    if title:
        qs = qs.filter(title__icontains=title)

    if director:
        qs = qs.filter(director__icontains=director)

    if cast:
        qs = qs.filter(cast__icontains=cast)

    if year:
        qs = qs.filter(release_year=year)

    if selectedGenres:
        genre_query = Q()
        for g in selectedGenres:
            # listed_in contains comma-separated genres
            genre_query |= Q(listed_in__icontains=g)
        qs = qs.filter(genre_query)

    # Used to filter by countries
    if selectedCountries:
        country_query = Q()
        for c in selectedCountries:
            country_query |= Q(country__icontains=c)
        qs = qs.filter(country_query)

    # Returns the final filtered list
    return qs
    