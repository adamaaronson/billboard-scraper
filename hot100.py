import billboard
import csv
import pandas as pd
import datetime as dt
import sys


def get_starting_date():
    hot100 = load_hot100()
    last_date = hot100['date'].max()
    return last_date.to_pydatetime().date() + dt.timedelta(weeks=1)


def scrape_hot100(starting_date: dt.date):
    date = starting_date
    if starting_date <= dt.date.today():
        print('Scraping from', date)

    with open('hot100.csv', 'a') as f:
        csv_writer = csv.writer(f)

        while date <= dt.date.today():
            chart = billboard.ChartData('hot-100', date.isoformat())
            for song in chart:
                csv_writer.writerow(
                    [
                        date,
                        song.rank,
                        song.title,
                        song.artist,
                        song.weeks,
                    ]
                )
            print('Wrote', date)

            date += dt.timedelta(weeks=1)


def update_hot100():
    starting_date = get_starting_date()
    scrape_hot100(starting_date)


def load_hot100():
    hot100 = pd.read_csv('hot100.csv')
    hot100 = hot100.astype({'rank': 'int32'})
    hot100 = hot100.drop('weeks', axis=1)
    hot100['date'] = pd.to_datetime(hot100['date'])

    return hot100


def search_hot100(pattern: str, filter_type: str):
    update_hot100()
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
