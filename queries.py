from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.master('local[4]')\
    .appName('test').\
    config('spark.executor.instances', 2)\
    .config('spark.executor.memory', '5g')\
    .config('spark.executor.cores', 2)\
    .getOrCreate()

path = '/data/titles.tsv'
path2 = '/data/aliases.tsv'
titles = spark.read.csv(path, sep=r'\t', nullValue='\\N', header=True)
aliases = spark.read.csv(path2, sep=r'\t', nullValue='\\N', header=True)

avg_movie_duration = titles.select(F.col('start_year'), F.col('runtime_minutes').cast('int')) \
    .groupby(F.col('start_year')) \
    .avg('runtime_minutes') \
    .where(F.col('start_year') >=2000)

top100_movie_duration = titles.join(aliases, 'title_id', 'inner') \
    .select(aliases.title, aliases.region, aliases.language, titles.runtime_minutes) \
    .where((F.col('start_year') >= 2000) & (aliases.title != titles.original_title)) \
    .sort(titles.runtime_minutes.desc()) \
    .limit(100)