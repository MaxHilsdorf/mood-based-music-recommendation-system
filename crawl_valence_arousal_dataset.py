# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 13:56:18 2021

@author: Max
"""
#################
## PREPARATION ##
#################

# Import modules
import sys
# If your authentification script is not in the project directory
# append its folder to sys.path
sys.path.append("../spotify_api_web_app")
import authorization
import pandas as pd
from tqdm import tqdm
import time

# Authorize and call access object "sp"
sp = authorization.authorize()

# Get all genres
genres = sp.recommendation_genre_seeds()

# Set number of recommendations per genre
n_recs = 100

# Initiate a dictionairy with all the information you want to crawl
data_dict = {"id":[], "genre":[], "track_name":[], "artist_name":[],
             "valence":[], "energy":[]}

################
## CRAWL DATA ##
################

# Get recs for every genre
for g in tqdm(genres):
    
    # Get n recommendations
    recs = sp.recommendations(genres = [g], limit = n_recs)
    # json-like string to dict
    recs = eval(recs.json().replace("null", "-999").replace("false", "False").replace("true", "True"))["tracks"]
    jh,jh,
    # Crawl data from each track
    for track in recs:
        # ID and Genre
        data_dict["id"].append(track["id"])
        data_dict["genre"].append(g)
        # Metadata
        track_meta = sp.track(track["id"])
        data_dict["track_name"].append(track_meta.name)
        data_dict["artist_name"].append(track_meta.album.artists[0].name)
        # Valence and energy
        track_features = sp.track_audio_features(track["id"])
        data_dict["valence"].append(track_features.valence)
        data_dict["energy"].append(track_features.energy)
        
        # Wait 0.2 seconds per track so that the api doesnt overheat
        time.sleep(0.2)
        
##################
## PROCESS DATA ##
##################

# Store data in dataframe
df = pd.DataFrame(data_dict)

# Drop duplicates
df.drop_duplicates(subset = "id", keep = "first", inplace = True)
df.to_csv("valence_arousal_dataset.csv", index = False)
    