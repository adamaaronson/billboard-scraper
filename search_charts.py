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


def scrape_billboard200(starting_date: dt.date):
    date = starting_date
    if starting_date <= dt.date.today():
        print('Scraping from', date)

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


def update_billboard200():
    starting_date = get_starting_date()
    scrape_billboard200(starting_date)


def load_hot100():
    hot100 = pd.read_csv('hot100.csv')
    hot100 = hot100.astype({'rank': 'int32'})
    hot100 = hot100.drop('weeks', axis=1)
    hot100['date'] = pd.to_datetime(hot100['date'])

    return hot100


def load_billboard200():
    billboard200 = pd.read_csv('billboard200.csv')
    billboard200 = billboard200.astype({'rank': 'int32'})
    billboard200 = billboard200.drop('weeks', axis=1)
    billboard200['date'] = pd.to_datetime(billboard200['date'])

    return billboard200


def to_peak_appearances(df: pd.DataFrame):
    # return only peak appearances of each song/album in the dataframe
    peak_appearances = df.loc[df.groupby(['title', 'artist'])['rank'].idxmin()]
    peak_appearances = peak_appearances.sort_values(
        by=['rank', 'date'], ascending=[True, False]
    )

    return peak_appearances


def search_hot100(pattern: str):
    update_hot100()
    update_billboard200()

    hot100 = load_hot100()
    billboard200 = load_billboard200()

    hot100 = hot100[
        hot100['artist'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
        | hot100['title'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
    ]
    hot100 = to_peak_appearances(hot100)
    hot100['type'] = 'song'

    billboard200 = billboard200[
        billboard200['artist'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
        | billboard200['title'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
    ]
    billboard200 = to_peak_appearances(billboard200)
    billboard200['type'] = 'album'

    all_results = pd.concat([hot100, billboard200])
    all_results = all_results[['date', 'type', 'rank', 'title', 'artist']]
    all_results = to_peak_appearances(all_results)

    print(all_results.head(n=20))


if __name__ == '__main__':
    search_hot100(sys.argv[1])
