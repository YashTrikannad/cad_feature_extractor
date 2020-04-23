import pandas as pd

df = pd.read_excel (r'/home/yash/PycharmProjects/cad_feature_detector/f2.xls')
df = df.sort_values('Name')
print(df)