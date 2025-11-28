from .models import NetflixTitles
from django.db.models import Q


def filterTitles(
        title=None,
        director=None,
        cast=None,
        year=None,
        selectedGenres=None,
        selectedCountries=None
):
    
    qs = NetflixTitles.objects.all()

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

    if selectedCountries:
        country_query = Q()
        for c in selectedCountries:
            country_query |= Q(country__icontains=c)
        qs = qs.filter(country_query)

    return qs
    