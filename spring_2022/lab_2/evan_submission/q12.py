import pandas as pd
appearances = pd.read_json('../data/lizzo_appearances.json')
appearances['talk_show'] = appearances.Title.str.lower().str.contains('show')
talk_appearances = appearances.loc[appearances.talk_show]
years_of_interest = talk_appearances['Year'].unique().astype(int)
lines = open('../data/wmbr.txt').readlines()
lines = map(lambda x: x.strip(), lines)
records = []
for line in lines:
    prefix, suffix = line.split(':', maxsplit=1)
    if prefix == 'Date':
        records.append([])
    records[-1].append(suffix)
df = pd.DataFrame(records, columns=['date', 'artist(s)', 'song', 'album', 'label', 'show', 'DJ'])
df.date = pd.to_datetime(df.date)
df = df.dropna(subset=['date'])
df['year'] = df.date.dt.year
df = df[df.year.isin(years_of_interest)]
df['is_lizzo'] = df['artist(s)'].str.lower().str.contains('lizzo')
df = df[df.is_lizzo]
# def caps_song(song):
#     out = []
#     for w in song.split():
#         for ix, char in enumerate(w):
#             if char.isalpha():
#                 out.append(w[:ix] + w[ix].upper() + w[ix+1:])
#                 break
#     return ' '.join(out)
# df['song'] = df['song'].apply(caps_song)
groups = df.groupby('song').agg('count').reset_index().\
    sort_values(['is_lizzo', 'song'], ascending=[False, True])
groups[['song', 'is_lizzo']].to_csv('q12.csv', index=False, header=False)
# with open('q12.csv', 'w') as f:
#     for (ix, song, count) in groups[['song', 'is_lizzo']].itertuples():
#         print(f'{song}, {count}', file=f)