import billboard
import datetime as dt
import csv

date = dt.date(1978, 5, 9)

with open('hot100.csv', 'a') as f:
    csv_writer = csv.writer(f)

    for _ in range(30000):
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
