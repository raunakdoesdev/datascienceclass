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
is_stranger_things = df.album.str.contains('Stranger Things')
djs = df.loc[is_stranger_things, 'DJ']
counts = djs.groupby(djs).count()
counts.name = 'count'
counts:pd.DataFrame = counts.reset_index().sort_values(['count', 'DJ'], ascending=[False, True])
counts.to_csv('q10.csv', index=False,header=False)