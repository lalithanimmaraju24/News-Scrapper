import datetime
import json
import pickle
from backend.utilites import cosine_similarity
from newsapi import NewsApiClient

global page_val
page_val = 1

filename_model = './static/finalized_model.pkl'
loaded_model = pickle.load(open(filename_model, 'rb'))
filename_vector = './static/vectorizer.pickle'
tfidf = pickle.load(open(filename_vector, 'rb'))
category_li = ['business', 'tech', 'politics', 'sport', 'entertainment']


def is_unique(text1, text2):
    if cosine_similarity(text1, text2) > 0.5:
        return False
    else:
        return True


def scrape_news():
    global page_val
    try:
        print(page_val)
        newsapi = NewsApiClient(api_key='fc96bec3a64941b581d2ecd95c74f7df')
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        all_articles = newsapi.get_everything(sources='bbc-news,the-verge,cnn',
                                              domains='bbc.com,techcrunch.com,edition.cnn.com',
                                              from_param=current_date,
                                              to=current_date,
                                              language='en',
                                              page=page_val)
        page_val += 1
        if len(all_articles['articles']) <= 0:
            print("articles are empty")
            page_val = 1
            return True
        # print(page_val, all_articles)
        unique_articles = []

        for i in range(len(all_articles['articles'])):
            not_unique = False
            for j in range(i + 1, len(all_articles['articles'])):
                text1 = all_articles['articles'][i]["title"]
                text2 = all_articles['articles'][j]["title"]
                if not is_unique(text1, text2):
                    not_unique = True
                    break
            if not not_unique:
                text_features = tfidf.transform([all_articles['articles'][i]['title']])
                predictions = loaded_model.predict(text_features)
                # print(predictions)
                news_category = category_li[int(predictions[0])]
                all_articles['articles'][i]['id'] = i
                all_articles['articles'][i]['category'] = news_category
                unique_articles.append(all_articles['articles'][i])


        with open("./static/news.json", "w", encoding="utf8") as outfile:
            json.dump(unique_articles, outfile)
        return True
    except Exception as ex:
        page_val = 1
        print(f"Exception in scraping news,{ex}")
        return False


if __name__ == '__main__':
    scrape_news()
