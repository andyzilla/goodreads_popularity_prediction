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
    - Converts str columns into lowercase
    - Converts RatingDistTotal into int and renames it as TotalReviews
    - Drops rows with NaN Description
    - Drops rows with year below Timestamp.min and above current year
    - Encodes NaN Publisher as "Unknown"
    - Replaces NaN languages by "eng" and drops all books that are not in "eng"
    - Drops unnecessary columns
    - Removes duplicated books, keeping min PublishYear, list of Publisher, median Rating and PagesNumber,
    max TotalReviews and longest description.
    """
    print("Lowering case of text fields")
    dataset['Name'] = dataset.Name.str.lower()
    dataset['Authors'] = dataset.Name.str.lower()
    dataset['Description'] = dataset.Description.str.lower()
    dataset['Publisher'] = dataset.Publisher.str.lower()

    print("Extracting TotalReviews")
    dataset['TotalReviews'] = dataset['RatingDistTotal'].str.replace("total:", "").astype(int)

    print("Dropping Null values")
    dataset = dataset.dropna(subset=['Description'])

    dataset = dataset.drop(dataset[dataset['PublishYear'] <= pd.Timestamp.min.year].index)
    dataset = dataset.drop(dataset[dataset['PublishYear'] >= date.today().year].index)

    print("Filling Null values")
    dataset['Publisher'] = dataset['Publisher'].fillna("Unknown")

    dataset['Language'] = dataset['Language'].fillna('eng')
    language_mask = dataset['Language'].str.startswith('en-')
    dataset.loc[language_mask, 'Language'] = 'eng'
    dataset = dataset[dataset.Language == 'eng']

    print("Dropping unused columns")
    dataset = dataset.drop(columns=['PublishMonth', 'Language', 'PublishDay',
                                    'ISBN', 'RatingDist1', 'RatingDist2',
                                    'RatingDist3', 'RatingDist4', 'RatingDist5',
                                    'Count of text reviews', 'RatingDistTotal',
                                    'CountsOfReview', 'Id'])

    print("Deduplicating")
    dataset = dataset.groupby(by=['Name', 'Authors']).agg({
        'PublishYear': 'min',
        'Publisher': list,
        'Rating': 'median',
        'PagesNumber': 'median',
        'TotalReviews': 'max',
        'Description': lambda series: series[series.str.len() == series.str.len().max()].iloc[0]
    })

    dataset.reset_index(inplace=True)
    dataset = dataset[dataset.Description != 'null']

    return dataset
