import pytest
import pandas as pd
import datatest as dt


@pytest.fixture(scope='module')
@dt.working_directory('/Users/mkortsev/imdb_project/data')
def df():
    return pd.read_csv('had_role.tsv', sep='\t', na_values='\\N')


@pytest.mark.mandatory
def test_columns(df):
    dt.validate(
        df.columns,
        {'title_id', 'name_id', 'role_'}
    )


def test_role(df):
    dt.validate.regex(df['role_'], r'^[A-Z]')
