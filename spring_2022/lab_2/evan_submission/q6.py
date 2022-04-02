import pandas as pd
df:pd.DataFrame = pd.read_csv('../data/salaries.csv', encoding='ISO-8859-1')
values:pd.Series = df['annual_bonus'].fillna(df['annual_bonus'].mean()).agg(['mean', 'std']).astype(int)
print(f'{values["mean"]:.0f}, {values["std"]:.0f}',file=open('q6.csv', 'w'))