import pytest
import pandas as pd
import datatest as dt


@pytest.fixture(scope='module')
@dt.working_directory('/Users/mkortsev/imdb_project/data')
def df():
    return pd.read_csv('names.tsv', sep='\t', na_values='\\N')


@pytest.mark.mandatory
def test_columns(df):
    dt.validate(
        df.columns,
        {'name_id', 'name_', 'birth_year', 'death_year'}
    )

