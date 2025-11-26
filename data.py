import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Is supposed to grab the amount of times a certain string shows in the csv and add it to an array
#Treats catagories, countries, ect with more then one entry different though, so action and action, comedy are different strings

df = pd.read_csv('netflix_titles.csv') # need to upload this into folder

filled_df = df.fillna("No info Available")

df_catagory_count = df['listed_in'].value_counts().head(5)

df_catagory_count_names = df_catagory_count.index.tolist()

df_catagory_count_numbers = df_catagory_count.values.tolist()

df_country_count = df['country'].value_counts().head(5)

df_country_count_names = df_country_count.index.tolist()

df_country_count_numbers = df_country_count.values.tolist()

df_rating_count = df['rating'].value_counts()

df_rating_count_names = df_rating_count.index.tolist()

df_rating_count_numbers = df_rating_count.values.tolist()


fig, axs = plt.subplots(3,1, figsize=(10,8))

axs[0].barh(df_catagory_count_names, df_catagory_count_numbers, color='g')
axs[0].set_title("Top 5 most popular genres on Netflix")

axs[1].bar(df_country_count_names, df_country_count_numbers, color='b')
axs[1].set_title("Top 5 countries with the most Netflix titles")

axs[2].pie(df_rating_count_numbers, labels=df_rating_count_names)
axs[2].set_title("Content Rating distribution")

plt.tight_layout()
plt.show()