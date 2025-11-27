# billboard-scraper

Search the history of Billboard's Hot 100 and Billboard 200 charts.

```
positional arguments:
  pattern               word, phrase, or regex pattern to search

options:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        maximum number of results to display
  --artist              only search artist names
  --album               only search album titles
  --song                only search song titles
```

```
>>> python3 search_charts.py word

             date   type  rank                                              title               artist
493406 2012-05-05  album     2                         Love Is A Four Letter Word           Jason Mraz
385007 2001-12-15  album     3                                       Word Of Mouf             Ludacris
147605 1986-11-22   song     6                                            Word Up                Cameo
95905  1976-12-25   song     6                 Sorry Seems To Be The Hardest Word           Elton John
91210  1973-10-06  album     6                                   Deliver The Word                  War
344814 1998-02-07  album    10  All I Have In This World, Are... My Balls And ...          Young Bleed
509621 2013-11-23  album    17                                      Word Of Mouth           The Wanted
157918 1988-11-12   song    19                                  A Word In Spanish           Elton John
399224 2003-04-26  album    20                                  Balls And My Word             Scarface
186626 1982-12-11  album    22                                      Word Of Mouth           Toni Basil
86632  1973-04-21  album    28                          Wattstax: The Living Word           Soundtrack
515837 2014-06-28  album    33                                               Real       The Word Alive
44033  1967-01-14   song    34                          There's Got To Be A Word!        The Innocence
394642 2002-11-16  album    38                           What's My Favorite Word?            Too $hort
292138 2014-08-02   song    39                                        Word Crimes  "Weird Al" Yankovic
41039  1966-06-18   song    40                    The Last Word In Lonesome Is Me          Eddy Arnold
139040 1985-03-30   song    41                                    The Word Is Out     Jermaine Stewart
72640  1972-07-08   song    41                                You Said A Bad Word              Joe Tex
24195  1966-09-17  album    46                          The Last Word In Lonesome          Eddy Arnold
495654 2012-07-21  album    50                                        Life Cycles       The Word Alive
```
