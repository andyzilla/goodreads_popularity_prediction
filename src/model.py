from sklearn import linear_model
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, RocCurveDisplay
from sklearn.pipeline import Pipeline


def evaluate_model(model, X_test=None, y_test=None):
    """

    Prints classification report and displays RocCurve

    :param model: scikitlearn classifier
    :param X_test: Dataframe containing Description and Name
    :param y_test: Series or nparray containing boolean class

    """
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    RocCurveDisplay.from_estimator(model, X_test, y_test)


def create_pipeline(params=None):
    """

    Creates pipeline with:
    1) ColumnTransformer: applies CountVectoriser to create a description_bow and title_bow.
    2) Model: uses the ColumnTransformer to convert variables,
    reduces dimensionality to 50 components using TruncatedSVD,
     and introduces a LogisticRegression classifier.

    :param params: if not None, overrides default parameters
    :return: model

    """
    column_trans = ColumnTransformer([
        ('description_bow', CountVectorizer(stop_words={'english'},
                                 max_df=0.05,
                                 min_df=50), 'Description'),
        ('title_bow', CountVectorizer(stop_words={'english'},
                                 max_df=0.05,
                                 min_df=50), 'Name'),
    ])
    model = Pipeline([
        ('column_transformer', column_trans),
        ('svd', TruncatedSVD(n_components=50)),
        ('classifier', linear_model.LogisticRegression(random_state=42)),
    ])

    if params:
        model.set_params(**params)

    return model