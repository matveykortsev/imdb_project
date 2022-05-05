from bs4 import BeautifulSoup
import requests
import logging
import pandas as pd
import os
import gzip
import shutil

IMDB_DATASETS_LINK = 'https://datasets.imdbws.com/'
DATA_PATH = os.path.join(os.getcwd(), 'data')


def get_zips(zips_link, data_path):
    """
    Download gziped datasets from imdb site
    """
    os.makedirs(data_path, exist_ok=True)
    r = requests.get(zips_link)
    page = BeautifulSoup(r.text, 'lxml')
    page_links = [elem['href'] for elem in page.find_all('a')]
    for link in page_links:
        if link.endswith('.gz'):
            req = requests.get(link)
            path_to_save = os.path.join(data_path, os.path.basename(link))
            with open(path_to_save, 'wb') as f:
                for chunk in req.iter_content(chunk_size=512 * 1024):
                    f.write(chunk)


def unzip_files(zip_path):
    """
    Unzip all gzipped files in folder.
    """
    for file in os.listdir(zip_path):
        if file.endswith(".gz"):
            in_file_path = os.path.join(zip_path, file)
            out_file_path = os.path.join(zip_path, file.replace('.gz', ''))
            logging.info('Unzipping ', in_file_path, ' to ', out_file_path)
            with gzip.open(in_file_path, 'rb') as f_in:
                with open(out_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(in_file_path)


def create_aliases(df):
    # title.akas.tsv
    logging.info("Creating aliases file...")
    aliases = df[['titleId', 'ordering', 'title', 'region', 'language', 'isOriginalTitle']]
    aliases = aliases.rename(columns={'titleId': 'title_id', 'isOriginalTitle': 'is_original_title'})
    aliases.to_csv('aliases.tsv', index=False, na_rep=r'\N', sep='\t')


def create_alias_types(df):
    # title.akas.tsv
    logging.info("Creating alias_types file")
    alias_types = df[['titleId', 'ordering', 'types']]
    alias_types = alias_types.rename(columns={'titleId': 'title_id', 'types': 'type'})
    alias_types = alias_types.dropna()
    alias_types.to_csv('alias_types.tsv', index=False, na_rep=r'\N', sep='\t')


def create_alias_attributes(df):
    # title.akas.tsv
    logging.info("Creating alias_attributes file...")
    alias_attributes = df[['titleId', 'ordering', 'attributes']]
    alias_attributes = alias_attributes.rename(columns={'titleId': 'title_id', 'attributes': 'attribute'})
    alias_attributes = alias_attributes.dropna()
    alias_attributes.to_csv('alias_attributes.tsv', index=False, na_rep=r'\N', sep='\t')


def create_directors_and_writers(df):
    # title.crew.tsv
    logging.info("Creating directors and writers files...")
    directors = df[['tconst', 'directors']]
    writers = df[['tconst', 'writers']]
    directors = directors.rename(columns={'tconst': 'title_id', 'directors': 'name_id'})
    writers = writers.rename(columns={'tconst': 'title_id', 'writers': 'name_id'})
    directors = directors.dropna()
    writers = writers.dropna()
    directors = directors.assign(name_id=directors.name_id.str.split(',')).explode('name_id').reset_index(drop=True)
    writers = writers.assign(name_id=writers.name_id.str.split(',')).explode('name_id').reset_index(drop=True)
    directors.to_csv('directors.tsv', index=False,na_rep=r'\N', sep='\t')
    writers.to_csv('writers.tsv', index=False, na_rep=r'\N', sep='\t')


def create_episode_belongs_to(df):
    # title.episode.tsv
    logging.info("Creating episode_belongs_to file...")
    episode_belongs_to = df.rename(columns={
        'tconst': 'title_id',
        'parentTconst': 'parent_tv_show_title_id',
        'seasonNumber': 'season_number',
        'episodeNumber': 'episode_number'
    })
    episode_belongs_to.to_csv('episode_belongs_to.tsv', index=False, na_rep=r'\N', sep='\t')


def create_names(df):
    logging.info("Creating names file...")
    names = df[['nconst', 'primaryName', 'birthYear', 'deathYear']]
    names = names.rename(columns={
        'nconst': 'name_id',
        'primaryName': 'name_',
        'birthYear': 'birth_year',
        'deathYear': 'death_year'
    })
    names.to_csv('names.tsv', index=False, na_rep=r'\N', sep='\t')


def create_name_worked_as(df):
    logging.info("Creating name_worked_as file...")
    name_worked_as = df[['nconst', 'primaryProfession']]
    name_worked_as = name_worked_as.dropna()
    name_worked_as = name_worked_as.rename(columns={
        'nconst': 'name_id',
        'primaryProfession': 'profession'
    })
    name_worked_as = name_worked_as.assign(profession=name_worked_as.profession.str.split(','))\
        .explode('profession')\
        .reset_index(drop=True)
    name_worked_as.to_csv('name_worked_as.tsv', index=False, na_rep=r'\N', sep='\t')


def create_known_for(df):
    logging.info("Creating known_for file...")
    known_for = df[['nconst', 'knownForTitles']]
    known_for = known_for.dropna()
    known_for = known_for.rename(columns={
        'nconst':'name_id',
        'knownForTitles': 'title_id'
    })
    known_for = known_for.assign(title_id=known_for.title_id.str.split(',')).explode('title_id').reset_index(drop=True)
    known_for.to_csv('known_for.tsv', index=False,na_rep=r'\N', sep='\t')


def create_principals(df):
    logging.info("Creating name_worked_as file...")
    principals = df[['tconst', 'ordering', 'nconst', 'category', 'job']]
    principals = principals.rename(columns={
        'tconst': 'title_id',
        'nconst': 'name_id',
        'category': 'job_category',
    })
    principals.to_csv('principals.tsv', index=False, na_rep=r'\N', sep='\t')


def create_had_role(df):
    logging.info("Creating had_role file...")
    had_role = df[['tconst', 'nconst', 'characters']]
    had_role = had_role.rename(columns={
        'tconst': 'title_id',
        'nconst': 'name_id',
        'characters': 'role_'
    })
    had_role = had_role.dropna()
    # removing [] from role
    had_role['role_'] = had_role['role_'].str.replace('[\"\[\]]', '', regex=True)
    had_role['role_'] = had_role['role_'].str.replace('\\', '|')
    had_role = had_role.assign(role_=had_role.role_.str.split(',')).explode('role_').reset_index(drop=True)
    # some data cleaning below
    had_role['role_'] = had_role['role_'].str.title()
    had_role['role_'] = had_role['role_'].str.replace('^ | $', '', regex=True)
    had_role.drop_duplicates(keep=False, inplace=True)
    had_role.to_csv('had_role.tsv', index=False, na_rep=r'\N', sep='\t')


def create_titles(df):
    logging.info("Creating titles file...")
    titles = df[['tconst', 'titleType', 'primaryTitle',
                 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes']]

    titles = titles.rename(columns={
        'tconst': 'title_id',
        'titleType': 'title_type',
        'primaryTitle': 'primary_title',
        'originalTitle': 'original_title',
        'isAdult': 'is_adult',
        'startYear': 'start_year',
        'endYear': 'end_year',
        'runtimeMinutes': 'runtime_minutes'
    })
    titles.to_csv('titles.tsv', index=False, na_rep=r'\N', sep='\t')


def create_title_genres(df):
    logging.info("Creating title_genres file...")
    title_genres = df[['tconst', 'genres']]
    title_genres = title_genres.rename(columns={
        'tconst': 'title_id',
        'genres': 'genre'
    })
    title_genres = title_genres.dropna()
    title_genres = title_genres.assign(genre=title_genres.genre.str.split(',')).explode('genre').reset_index(drop=True)
    title_genres.to_csv('title_genres.tsv', index=False, na_rep=r'\N', sep='\t')


def create_title_ratings(df):
    logging.info("Creating title_ratings file...")
    title_ratings = df.rename(columns={
        'tconst':'title_id',
        'averageRating':'average_rating',
        'numVotes':'num_votes'
    })
    title_ratings.to_csv('title_ratings.tsv', index=False, na_rep=r'\N', sep='\t')


if __name__ == "__main__":
    if not os.path.isdir(DATA_PATH):
        os.makedirs(DATA_PATH, exist_ok=True)
    if not os.listdir(DATA_PATH):
        get_zips(IMDB_DATASETS_LINK, DATA_PATH)
        unzip_files(DATA_PATH)
    logging.info('\n', 'Reading title.akas.tsv ...', '\n')
    title_akas = pd.read_csv(os.path.join(DATA_PATH, 'title.akas.tsv'),
                             dtype={'titleId': 'str',
                                    'ordering': 'int',
                                    'title': 'str',
                                    'region': 'str',
                                    'language': 'str',
                                    'types': 'str',
                                    'attributes': 'str',
                                    'isOriginalTitle': 'Int64'},
                             sep='\t',
                             na_values='\\N',
                             quoting=3
                             )
    create_aliases(title_akas)
    create_alias_types(title_akas)
    create_alias_attributes(title_akas)
    del title_akas
    os.remove(os.path.join(DATA_PATH, 'title.akas.tsv'))
    logging.info('\n', 'Reading title.crew.tsv', '\n')
    title_crew = pd.read_csv(os.path.join(DATA_PATH, 'title.crew.tsv'), sep='\t', na_values='\\N')
    create_directors_and_writers(title_crew)
    del title_crew
    os.remove(os.path.join(DATA_PATH, 'title.crew.tsv'))
    logging.info('\n', 'Reading title.episode.tsv ...', '\n')
    title_episode = pd.read_csv(os.path.join(DATA_PATH, 'title.episode.tsv'),
                                dtype={'tconst': 'str',
                                       'parentTconst': 'str',
                                       'seasonNumber': 'Int64',
                                       'episodeNumber': 'Int64'},
                                sep='\t',
                                na_values='\\N')
    create_episode_belongs_to(title_episode)
    del title_episode
    os.remove(os.path.join(DATA_PATH, 'title.episode.tsv'))
    logging.info('\n', 'Reading name.basics.tsv ...', '\n')
    name_basics = pd.read_csv(os.path.join(DATA_PATH, 'name.basics.tsv'),
                              dtype={'nconst': 'str',
                                     'primaryName': 'str',
                                     'birthYear': 'Int64',
                                     'deathYear': 'Int64',
                                     'primaryProfession': 'str',
                                     'knownForTitles': 'str'},
                              sep='\t', na_values='\\N')
    create_names(name_basics)
    create_name_worked_as(name_basics)
    create_known_for(name_basics)
    del name_basics
    os.remove(os.path.join(DATA_PATH, 'name.basics.tsv'))
    logging.info('\n', 'Reading title.principals.tsv ...', '\n')
    title_principals = pd.read_csv(os.path.join(DATA_PATH, 'title.principals.tsv'), sep='\t', na_values='\\N')
    create_principals(title_principals)
    create_had_role(title_principals)
    del title_principals
    os.remove(os.path.join(DATA_PATH, 'title.principals.tsv'))
    logging.info('\n', 'Reading title.basics.tsv ...', '\n')
    title_basics = pd.read_csv(os.path.join(DATA_PATH, 'title.basics.tsv'),
                               dtype={'tconst': 'str',
                                      'titleType': 'str',
                                      'primaryTitle': 'str',
                                      'originalTitle': 'str',
                                      'isAdult': 'int',
                                      'startYear': 'Int64',
                                      'endYear': 'Int64',
                                      'runtimeMinutes': 'Int64', 'genres': 'str'},
                               sep='\t', na_values='\\N', quoting=3)
    create_titles(title_basics)
    create_title_genres(title_basics)
    del title_basics
    os.remove(os.path.join(DATA_PATH, 'title.basics.tsv'))
    logging.info('\n', 'Reading title.ratings.tsv ...', '\n')
    title_ratings = pd.read_csv(os.path.join(DATA_PATH, 'title.ratings.tsv'), sep='\t', na_values='\\N')
    create_title_ratings(title_ratings)
    del title_ratings
    os.remove(os.path.join(DATA_PATH, 'title.ratings.tsv'))