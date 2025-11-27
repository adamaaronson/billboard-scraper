import argparse
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


def search_chart(chart: pd.DataFrame, pattern: str, artist: bool, title: bool):
    return chart[
        (
            artist
            & chart['artist'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
        )
        | (
            title
            & chart['title'].str.contains(rf'\b{pattern}\b', case=False, regex=True)
        )
    ]


def search_charts(args: dict):
    update_hot100()
    update_billboard200()

    hot100 = load_hot100()
    billboard200 = load_billboard200()

    search_all = not (args.search_artists or args.search_albums or args.search_songs)

    hot100 = search_chart(
        hot100,
        args.pattern,
        search_all or args.search_artists,
        search_all or args.search_songs,
    )
    hot100 = to_peak_appearances(hot100)
    hot100['type'] = 'song'

    billboard200 = search_chart(
        billboard200,
        args.pattern,
        search_all or args.search_artists,
        search_all or args.search_albums,
    )
    billboard200 = to_peak_appearances(billboard200)
    billboard200['type'] = 'album'

    all_results = pd.concat([hot100, billboard200])
    all_results = all_results[['date', 'type', 'rank', 'title', 'artist']]
    all_results = to_peak_appearances(all_results)

    print(all_results.head(n=30).to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description='Billboard chart search')

    parser.add_argument(
        dest='pattern',
        type=str,
        help='word, phrase, or regex pattern to search',
    )
    parser.add_argument(
        '-n',
        '--number',
        type=int,
        help='maximum number of results to display',
    )

    result_types = parser.add_mutually_exclusive_group()
    result_types.add_argument(
        '--artist',
        dest='search_artists',
        default=False,
        action='store_true',
        help='only search artist names',
    )
    result_types.add_argument(
        '--album',
        dest='search_albums',
        default=False,
        action='store_true',
        help='only search album titles',
    )
    result_types.add_argument(
        '--song',
        dest='search_songs',
        default=False,
        action='store_true',
        help='only search song titles',
    )

    args = parser.parse_args()

    search_charts(args)


if __name__ == '__main__':
    main()
