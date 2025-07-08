# Project Initial Setup (with some help of Claude)

Problems:

1) The original issue was a `ModuleNotFoundError: No module named 'psycopg2'` when running `alembic upgrade head`.

Add psycopg2-binary = "^2.9.5" to pyproject.toml

2) Migration not able to find files 
sqlalchemy.exc.OperationalError: (psycopg2.errors.UndefinedFile) could not open file "/home/dcorreia/repos/hrf-universe-home-task/migrations/versions/../data/standard_job_family.csv" for reading: No such file or directory

Opted for quick fix of copying files because it is not the focus at the moment to automate this

docker cp migrations/data/standard_job_family.csv hrf_universe_postgres:/tmp/standard_job_family.csv
docker cp migrations/data/standard_job.csv hrf_universe_postgres:/tmp/standard_job.csv
docker cp migrations/data/job_posting.csv hrf_universe_postgres:/tmp/job_posting.csv