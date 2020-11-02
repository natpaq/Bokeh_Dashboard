import pandas as dd
chunksize=1000
for chunk in dd.read_csv('only_in_2020.csv', chunksize=chunksize,  delimiter=",", encoding="utf-8", usecols=[1,2,8]):
    chunk.dropna().to_csv('filtered_cols_2020.csv', mode='a', index=False)
