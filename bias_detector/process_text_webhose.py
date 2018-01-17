import json
news_sources = {
    'breitbart' : 1,
    'cbs' : 0,
    'foxnews' : 1,
    'huffingtonpost' : 0,
    'nbcnews' : 0,
    'nytimes' : 0,
    'npr' : 0,
    'theatlantic': 0,
    'vox' : 0,
    'washingtonpost' : 0,
}

def main():
    with open("webhose_news_formatted.csv", 'w+') as fw:
        for i in range(1,499611):
            with open("webhose/news_" + str(i).zfill(7) + ".json") as f:
                data = json.load(f)
                curr_source = data['thread']['site_full']
                for news_source in news_sources:
                    if news_source in curr_source: #current source is from one of the desired news sources
                        fw.write(str(news_sources[news_source]) + '\t' + data['text'].replace('\n', ' ') + '\n')
                        break



if __name__ == '__main__':
    main()
