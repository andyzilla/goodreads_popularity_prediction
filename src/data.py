import pandas as pd
from sklearn.model_selection import train_test_split

REVIEWS_THRESHOLD = 500


def load_train_test_sets(reviews_threshold=REVIEWS_THRESHOLD):
    df = pd.read_csv('../data/clean_dataset.csv', index_col=0)
    print(
        f'Proportion of popular books in the dataset: {round((df.TotalReviews > reviews_threshold).sum() / df.index.size, 2)}')
    print((df.TotalReviews > REVIEWS_THRESHOLD).sum())
    input_columns = [column for column in df.columns if column != 'TotalReviews']
    X, y = df[input_columns], df.TotalReviews > REVIEWS_THRESHOLD
    return train_test_split(X, y, test_size=0.1, random_state=42)
