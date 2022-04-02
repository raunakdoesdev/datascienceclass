import pandas as pd
import numpy as np
df:pd.DataFrame = pd.read_csv('../data/salaries.csv', encoding='ISO-8859-1')
non_zero:pd.DataFrame = df[df.annual_bonus > 0]
ratio = (non_zero['annual_bonus'] / non_zero['annual_base_pay']).mean()
df['imputed_annual_bonus'] =\
    np.where(df.annual_bonus.isna(), df.annual_base_pay * ratio, df.annual_bonus)
values = df['imputed_annual_bonus'].agg(['mean', 'std']).round(0)
print(f'{values["mean"]:.0f}, {values["std"]:.0f}',file=open('q7.csv', 'w'))
