import sys
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from db import get_session

def query(min_sample):
    return f"""
            insert into days_to_hire (standard_job_id, country_code, average, minimum, maximum, count)
            with percentil as (
                select 
                percentile_disc(0.1) within group (order by days_to_hire) perc_10,
                percentile_disc(0.9) within group (order by days_to_hire) perc_90
                from job_posting
                where days_to_hire is not null)
            , valid_values as (
                select standard_job_id,
                    country_code,
                    days_to_hire
                from job_posting
                where days_to_hire between (select perc_10 from percentil) and (select perc_90 from percentil))
            , country_averages as (
                select standard_job_id,
                    country_code,
                    avg(days_to_hire) average,
                    min(days_to_hire) minimum,
                    max(days_to_hire) maximum,
                    count(days_to_hire) samples
                from valid_values
                where country_code is not null
                group by standard_job_id,
                    country_code		
                having count(*) >= {min_sample})
            , global_averages as (
                select standard_job_id,
                    'WW' country_code,
                    avg(days_to_hire) average,
                    min(days_to_hire) minimum,
                    max(days_to_hire) maximum,
                    count(days_to_hire) samples
                from valid_values
                group by standard_job_id
                having count(*) >= {min_sample})
            select standard_job_id,
                country_code,
                average,
                minimum,
                maximum,
                samples
            from country_averages
            union 
            select standard_job_id,
                country_code,
                average,
                minimum,
                maximum,
                samples
            from global_averages;
        """

def calculate_days_to_hire(min_sample=5):
    session = get_session()

    try:
        print("Clear table")
        session.execute(text("truncate table days_to_hire"))

        print("Calculating days to hire stats")
        session.execute(text(query(min_sample)))

        session.commit()
        print("Done!")

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        session.rollback()
        return False
        
    finally:
        session.close()

def main():
    min_sample = 5

    if len(sys.argv) > 1 and sys.argv[1].startswith('--min-samples='):
        try:
            min_sample = int(sys.argv[1].split('=')[1])
        except ValueError:
            print("Error: min-samples must be a number")
            return

    calculate_days_to_hire(min_sample)

if __name__ == '__main__':
    main()

