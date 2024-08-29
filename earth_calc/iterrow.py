# import pandas as pd
#
# df = pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]})
# df = df.reset_index()  # make sure indexes pair with number of rows
# print(df)
#
# for index, row in df.iterrows():
#     print(index)
#     print(row['c1'], row['c2'])

import pandas as pd

data = {
    'Tracker_ID': [1, 2, 3],
    'x': [4, 5, 6],
    'y': [7, 8, 9]
}
df = pd.DataFrame(data)
i = 0
crap = df.itertuples()
print(crap)
# for i in df.itertuples() :
#     counter = i +1
#     print(counter)

    # itertuples goes through everything