import glob
from datetime import date

import pandas as pd
from tqdm import tqdm


def load_dataset(sample_frac=None) -> pd.DataFrame:
    """
    Loads the goodreads dataset
    :param sample_frac: it must be [0..1] value
    :return: the complete goodreads dataset (except those files without description)
    """
    block_list = ['../data.py/book1-100k.csv',
                  '../data.py/book100k-200k.csv',
                  '../data.py/book200k-300k.csv',
                  '../data.py/book300k-400k.csv',
                  '../data.py/book400k-500k.csv',
                  '../data.py/book500k-600k.csv',
                  ]
    file_names = glob.glob('../data/book*.csv')

    dfs = []

    for file_name in tqdm(file_names):
        if file_name not in block_list:
            df = pd.read_csv(file_name)
            if sample_frac:
                df = df.sample(frac=sample_frac)
            if 'pagesNumber' in df.columns:
                df.rename(columns={'pagesNumber': 'PagesNumber'}, inplace=True)
            dfs.append(df)

    df = pd.concat(dfs)
    return df


def clean_dataset(dataset):
    """
    Cleans the dataset
    TODO: enumerate all cleaning steps, check EDA for details on these changes
    """

    dataset['TotalReviews'] = dataset['RatingDistTotal'].str.replace("total:", "").astype(int)

    dataset = dataset.dropna(subset= 'Description')
    dataset = dataset.drop(dataset[dataset['PublishYear'] <= pd.Timestamp.min.year].index)
    dataset = dataset.drop(dataset[dataset['PublishYear'] >= date.today().year].index)

    dataset['Publisher'] = dataset['Publisher'].fillna("Unknown")
    dataset['Language'] = dataset['Language'].fillna('eng')

    language_mask = dataset['Language'].str.startswith('en-')
    dataset.loc[language_mask, 'Language'] = 'eng'

    dataset = dataset[dataset.Language == 'eng']

    dataset = dataset.drop(columns=['PublishMonth', 'Language', 'PublishDay', 'ISBN', 'RatingDist1', 'RatingDist2', 'RatingDist3', 'RatingDist4', 'RatingDist5', 'Count of text reviews', 'RatingDistTotal', 'CountsOfReview', 'Id'])

    dataset = dataset.groupby(by=['Name', 'Authors']).agg({
        'PublishYear': 'min',
        'Publisher': list,
        'Rating': 'median',
        'PagesNumber': 'median',
        'TotalReviews': 'max',
        'Description': lambda series: series[series.str.len() == series.str.len().max()]
    })

    dataset.reset_index(inplace=True)

    return dataset
