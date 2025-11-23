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


def scrape_billboard200():
    date = dt.date(1975, 8, 23)

    with open('billboard200.csv', 'a') as f:
        csv_writer = csv.writer(f)

        while date <= dt.date.today():
            chart = billboard.ChartData('billboard-200', date.isoformat(), timeout=None)
            for album in chart:
                csv_writer.writerow(
                    [
                        date,
                        album.rank,
                        album.title,
                        album.artist,
                        album.weeks,
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


def load_billboard200():
    billboard200 = pd.read_csv('billboard200.csv')
    billboard200 = billboard200.astype({'rank': 'int32'})
    # billboard200 = billboard200.drop('weeks', axis=1)
    billboard200['date'] = pd.to_datetime(billboard200['date'])

    return billboard200


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


def cleanup_billboard200():
    billboard200 = load_billboard200()
    billboard200 = billboard200.drop_duplicates()

    billboard200current = pd.read_csv('billboard-200-current.csv')
    billboard200current = billboard200current.astype({'current_week': 'int32'})
    billboard200current = billboard200current.drop('last_week', axis=1)
    billboard200current = billboard200current.drop('peak_pos', axis=1)
    billboard200current['chart_week'] = pd.to_datetime(
        billboard200current['chart_week']
    )
    billboard200current = billboard200current.rename(
        columns={
            'chart_week': 'date',
            'current_week': 'rank',
            'performer': 'artist',
            'wks_on_chart': 'weeks',
        }
    )
    billboard200current = billboard200current.sort_values(
        by=['date', 'rank'], ascending=[True, True]
    )
    billboard200current = billboard200current[
        billboard200current['date'] > pd.to_datetime(dt.date(1975, 10, 11))
    ]

    billboard200combined = pd.concat([billboard200, billboard200current])
    billboard200combined = billboard200combined.sort_values(
        by=['date', 'rank'], ascending=[True, True]
    )

    billboard200combined.to_csv('billboard200combined.csv', index=False)


if __name__ == '__main__':
    cleanup_billboard200()
    # search_hot100(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '')
