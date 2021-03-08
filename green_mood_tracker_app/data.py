# from green_mood_tracker.params import BUCKET_NAME, MODEL_NAME, MODEL_VERSION, UK_LIST, USA_LIST
import pandas as pd
# import os
# from pathlib import Path
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import download
# from green_mood_tracker.twint_class import TWINT
# import datetime
download('wordnet')
download('stopwords')
download('punkt')


def clean(df, column='text'):

    cachedStopWords = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()

    df[column] = df[column].apply(lambda x1: " ".join(
        filter(lambda x2: x2[0] != '@', x1.split())))
    df[column] = df[column].apply(lambda x: x.translate(
        str.maketrans('', '', string.punctuation)))
    df[column] = df[column].apply(lambda x: x.translate(
        str.maketrans('', '', string.digits)))
    df[column] = df[column].apply(lambda x: x.lower())
    df[column] = df[column].apply(lambda x: ' '.join(
        [lemmatizer.lemmatize(word) for word in x.split()]))
    df[column] = df[column].apply(lambda x: ' '.join(
        [word for word in x.split() if word not in cachedStopWords]))

    return df



# def get_twint_data(filepath, country, topic, since, until):

#     if country == 'USA':
#         cities_list = USA_LIST
#     elif country == 'UK':
#         # cities_list = UK_LIST
#         cities_list = ['London']

#     kwargs = dict(
#         keywords=topic.lower().split(),
#         cities=cities_list,
#         since=f'{str(since)} 12:00:00',
#         store_csv=False,
#         limit=200000
#     )

#     t = TWINT(**kwargs)

#     df = t.city_df()
#     df['date'] = df['date'].apply(
#         lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())
#     df = df[(since < df['date'])
#             & (df['date'] < until)]
#     filepath = 'green_mood_tracker/raw_data/' + filepath
#     path = Path(filepath)

#     if(not os.path.isdir(str(path.parent))):
#         os.makedirs(str(path.parent))
#     df.to_csv(filepath, index=False)


if __name__ == '__main__':
    params = dict(nrows=10000,
                  # set to False to get data from GCP (Storage or BigQuery)
                  local=True,
                  binary=True)
    df = get_data(**params)
    print(df.shape)
