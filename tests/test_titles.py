import pytest
import pandas as pd
import datatest as dt
import math


@pytest.fixture(scope='module')
@dt.working_directory('/Users/mkortsev/imdb_project/data')
def df():
    return pd.read_csv('titles.tsv', sep='\t', na_values='\\N')


@pytest.mark.mandatory
def test_columns(df):
    dt.validate(
        df.columns,
        {'title_id',
         'title_type',
         'primary_title',
         'original_title',
         'is_adult',
         'start_year',
         'end_year',
         'runtime_minutes'},
    )


def is_correct_runtime(x):
    return x >= 0


def test_runtime(df):
    with dt.accepted(dt.Extra(math.nan)):
        dt.validate(df['runtime_minutes'], is_correct_runtime)
