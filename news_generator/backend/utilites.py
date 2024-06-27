import os
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# To measure the similarity between
# two sentences using cosine similarity.
def cosine_similarity(text1, text2):
    lower_text1 = text1.lower()
    lower_text2 = text2.lower()
    # tokenization
    text1_list = word_tokenize(lower_text1)
    text2_list = word_tokenize(lower_text2)

    # sw contains the list of stopwords
    sw = stopwords.words('english')
    l1 = []
    l2 = []

    # remove stop words from the string
    X_set = {w for w in text1_list if not w in sw}
    Y_set = {w for w in text2_list if not w in sw}

    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)

    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    if sum(l1) < 1 or sum(l2) < 1:
        return 0.0
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    # print("similarity: ", cosine)
    return cosine


def sort_by_user_interest(news_list, user_id):
    updated_news_list = []
    if os.path.exists("./static/user_models/" + str(user_id) + ".csv"):
        data = pd.read_csv("./static/user_models/" + str(user_id) + ".csv")
        for item in news_list:
            average_score = 0
            for i in range(data.shape[0]):
                saved_title = data.iloc[i]['title']
                # saved_description = data.iloc[i]['description']
                # print(saved_title+"|"+item['title'])
                title_score = cosine_similarity(saved_title, item['title'])
                # description_score = cosine_similarity(saved_description, item['description'])
                average_score += title_score  # + description_score
                # print(title_score)
            # print(average_score, data.shape[0])
            similarity_score = average_score / data.shape[0]
            updated_news_list.append((item, similarity_score))
        updated_news_list = sorted(updated_news_list, key=lambda x: x[1])
        out_news = []
        for news in updated_news_list:
            print(news[1])
            if news[1] >= 0.10:
                print(news)
                news[0]['recommend'] = True
                out_news.append(news[0])
            else:
                news[0]['recommend'] = False
                out_news.append(news[0])
        return out_news
    else:
        for news in news_list:
            news['recommend'] = False
        return news_list


def add_user_data(user_id, title, description):
    if not os.path.exists("./static/user_models/" + str(user_id) + ".csv"):
        data = pd.DataFrame({"title": [title], 'description': [description]}, columns=['title', 'description'])
        data.to_csv("./static/user_models/" + str(user_id) + ".csv", index=False)
    else:
        data = pd.read_csv("./static/user_models/" + str(user_id) + ".csv")
        # print(data)
        data.loc[data.shape[0]] = [title, description]
        data.to_csv("./static/user_models/" + str(user_id) + ".csv", index=False)
