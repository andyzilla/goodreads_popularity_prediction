import glob

import pandas as pd
from tqdm import tqdm


def load_dataset(sample_frac=None) -> pd.DataFrame:
    """
    Loads the goodreads dataset
    :param sample_frac: it must be [0..1] value
    :return: the complete goodreads dataset (except those files without description)
    """
    block_list = ['../data/book1-100k.csv',
                  '../data/book100k-200k.csv',
                  '../data/book200k-300k.csv',
                  '../data/book300k-400k.csv',
                  '../data/book400k-500k.csv',
                  '../data/book500k-600k.csv',
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
            df['filename'] = file_name
            dfs.append(df)

    df = pd.concat(dfs)
    return df
