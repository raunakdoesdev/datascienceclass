import pandas as pd
df:pd.DataFrame = pd.read_csv('../data/salaries.csv', encoding='ISO-8859-1')
values = df['annual_bonus'].agg(['mean', 'std']).round(0)
print(f'{values["mean"]:.0f}, {values["std"]:.0f}',file=open('q5a.csv', 'w'))