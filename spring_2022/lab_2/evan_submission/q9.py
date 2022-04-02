import pandas as pd
import re
# Cleaning script
lines = open('../data/wmbr.txt').readlines()
records = []
for line in lines:
    prefix, suffix = line.split(':', maxsplit=1)
    if prefix == 'Date':
        records.append([])
    records[-1].append(suffix)
df = pd.DataFrame(records, columns=['date', 'artist(s)', 'song', 'album', 'label', 'show', 'DJ'])
# Extracting artists
is_live = df.song.str.lower().str.contains('live') | df.album.str.lower().str.contains('live')
unique_artists = df.loc[is_live, 'artist(s)'].unique()
title_case_artists = [artist.title() for artist in unique_artists]
with open('q9.csv', 'w') as f:
    for artist in sorted(title_case_artists):
        assert(isinstance(artist, str))
        print(artist.strip().title(), file=f)
# MULTI_ARTIST_INDICATORS = [',', 'and', '&']
# artist_set = set()
# for artist_s in df['artist(s)'].unique():
#     for artist in re.split("|".join(MULTI_ARTIST_INDICATORS), artist_s):
#         artist_set.add(artist.strip())
# MANUAL_DUPLICATES = {'Billie Ellish', 'James Black', 'ROSALIA', 'billie eilish'}
# unique_artists = artist_set.difference(set())
# unique_artists = sorted(list(unique_artists))
# with open('q9.csv', 'w') as f:
#     for artist in unique_artists:
#         print(artist, file=f)