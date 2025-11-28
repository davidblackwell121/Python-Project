import pandas as pd
from  netflixTitlesApp.models import NetflixTitles
def load_data():
        df = pd.read_csv("netflixTitlesApp/netflix_titles.csv")
        filled_df = df.fillna("No Info Available")
        
        for _, row in filled_df.iterrows():
            NetflixTitles.objects.create(
                show_id=row["show_id"],
                type=row["type"],
                title=row["title"],
                director=row["director"],
                cast=row["cast"],
                country=row["country"],
                date_added=row["date_added"],
                release_year=row["release_year"],
                rating=row["rating"],
                duration=row["duration"],
                listed_in=row["listed_in"],
                description=row["description"]
        )
        print("Data Loaded Successfully!")

load_data()

