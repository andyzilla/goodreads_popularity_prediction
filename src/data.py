import pandas as pd
from sklearn.model_selection import train_test_split

REVIEWS_THRESHOLD = 500


def load_train_test_sets(reviews_threshold=REVIEWS_THRESHOLD, debug=False):
    """
    Splits dataset into train and test, using TotalReviews as y.

    :param reviews_threshold: threshold to classify a book as a success or not, default value is 500.
    :param debug: if true returns amount of reviews in X
    :return: X_train, X_test, y_train, y_test
    """
    df = pd.read_csv('../data/clean_dataset.csv', index_col=0)
    print(
        f'Proportion of popular books in the dataset: {round((df.TotalReviews > reviews_threshold).sum() / df.index.size, 2)}')
    print((df.TotalReviews > REVIEWS_THRESHOLD).sum())
    input_columns = [column for column in df.columns if debug or column != 'TotalReviews']
    X, y = df[input_columns], df.TotalReviews > REVIEWS_THRESHOLD
    return train_test_split(X, y, test_size=0.1, random_state=42)
