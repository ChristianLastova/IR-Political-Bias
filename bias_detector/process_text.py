import csv
import sys

news_sources = {
    'New York Times' : 0,
    'CNN' : 0,
    'Atlantic' : 0,
    'Breitbart' : 1,
    'Business Insider': 0,
    'Talking Points Memo' : 0,
    'Fox News' : 1,
    'New York Post' : 1,
    'National Review' : 1,
    'Buzzfeed News': 0,
    'Guardian': 0,
    'Reuters': 0,
    'Vox': 0,
    'NPR' : 0,
    'Washington Post': 0,
}

csv.field_size_limit(sys.maxsize)
for i in range(1,4):
    with open("all-the-news/articles" + str(i) + ".csv") as f:
        reader = csv.reader(f, delimiter=",")
        with open("all-the-news/articles_format" + str(i) + ".csv", "w+") as fw:
            for i, line in enumerate(reader):
                if i == 0:
                    continue
                publication = line[3]
                content = line[-1].replace('\n', ' ')
                bias = news_sources[publication]
                fw.write(str(bias) + "\t" + content + "\n")
