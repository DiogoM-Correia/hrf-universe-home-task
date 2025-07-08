Resume on how to run the new developments

1) Calculate days to hire:
In home task, run: python3 home_task/days_to_hire_calculation.py

2) Get days to hire api:

#This will start the server 
uvicorn home_task.get_stats:app --reload

Then open browser with link for the search you wish.

For country DE and standard job X1 (replace x1 with your standar job)
http://127.0.0.1:8000/days-to-hire/X1?country_code=DE

If you want world view:
http://127.0.0.1:8000/days-to-hire/X1