import pandas as pd
import datetime as dt
import sys


def load_hot100():
    hot100 = pd.read_csv('hot100.csv')
    hot100 = hot100.astype({'rank': 'int32'})
    hot100 = hot100.drop('weeks', axis=1)
    hot100['date'] = pd.to_datetime(hot100['date'])

    return hot100


def search_hot100(pattern: str, filter_type: str):
    hot100 = load_hot100()

    # filter by pattern
    if filter_type.lower().startswith('a'):
        hot100 = hot100[
            hot100['artist'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
        ]
    elif filter_type.lower().startswith('s') or filter_type.lower().startswith('t'):
        hot100 = hot100[
            hot100['title'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
        ]
    else:
        hot100 = hot100[
            hot100['artist'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
            | hot100['title'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
        ]

    # filter by top appearance of each song by rank
    hot100 = hot100.loc[hot100.groupby(['title', 'artist'])['rank'].idxmin()]
    hot100 = hot100.sort_values(by=['rank', 'date'], ascending=[True, False])

    print(hot100.head(n=20))


if __name__ == '__main__':
    search_hot100(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '')
