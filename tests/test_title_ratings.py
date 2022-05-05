import pytest
import pandas as pd
import datatest as dt


@pytest.fixture(scope='module')
@dt.working_directory('/Users/mkortsev/imdb_project/data')
def df():
    return pd.read_csv('title_ratings.tsv', sep='\t', na_values='\\N')


@pytest.mark.mandatory
def test_columns(df):
    dt.validate(
        df.columns,
        {'title_id', 'average_rating', 'num_votes'}
    )


def is_correct_rating(x):
    return 0 <= x <= 10


def test_rating(df):
    dt.validate(df['average_rating'], is_correct_rating)
