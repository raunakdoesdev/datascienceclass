import re

import pandas as pd

lines = open('../data/wmbr.txt').readlines()
records = []
for line in lines:
    prefix, suffix = line.split(':', maxsplit=1)
    if prefix == 'Date':
        records.append([])
    records[-1].append(suffix)
df = pd.DataFrame(records, columns=['date', 'artist(s)', 'song', 'album', 'label', 'show', 'DJ'])
MULTI_ARTIST_INDICATORS = [',', 'and', '&']
artist_set = set()
for artist_s in df['artist(s)'].unique():
    for artist in re.split("|".join(MULTI_ARTIST_INDICATORS), artist_s):
        artist_set.add(artist.strip().lower())
MANUAL_DUPLICATES = {'Billie Ellish', 'James Black', 'ROSALIA', 'billie eilish'}
unique_artists = artist_set.difference(set())
unique_artists = sorted(list(unique_artists))

top = pd.read_csv('../data/top2018.csv')
top['played_at_wmbr'] = [artist.lower() in unique_artists for artist in top.artists]
top = top.loc[top.played_at_wmbr]

top.sort_values('danceability', ascending=False).head(1)[['artists', 'name', 'danceability']].\
    to_csv('q13.csv', index=False, header=False)
