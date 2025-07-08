from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from .db import get_session

app = FastAPI()

class DaysToHire(BaseModel):
    standard_job_id: str
    country_code: str
    min_days: float
    avg_days: float
    max_days: float
    job_postings_number: int

@app.get("/days-to-hire/{standard_job_id}", response_model=DaysToHire)
def get_days_to_hire(standard_job_id: str, country_code: str = Query("WW", description="Country code")):
    session = get_session()

    sql = """
            SELECT standard_job_id, country_code, minimum, average, maximum, count
            FROM days_to_hire 
            WHERE standard_job_id = :standard_job_id AND country_code = :country_code
        """

    result = session.execute(sql, {"standard_job_id": standard_job_id, "country_code": country_code}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="No data found")

    return DaysToHire(
        standard_job_id=result[0],
        country_code=result[1],
        min_days=float(result[2]),
        avg_days=float(result[3]),
        max_days=float(result[4]),
        job_postings_number=result[5]
    ) 