import pandas as pd
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
BILLIE_NAMES = {'Billie Eilish', 'billie eilish', 'Billie Ellish'}
df['is_billie'] = [a in BILLIE_NAMES for a in df['artist(s)']]
df['year'] = df.date.dt.year
grouped = df.groupby(['year']).agg({'is_billie': 'mean'}).loc[[2017, 2018, 2019]].sort_index(ascending=False)
with open('q11.csv', 'w') as f:
    for (year, ratio) in grouped.itertuples():
        print(f'{year}, {round(ratio, 4)}', file=f)
