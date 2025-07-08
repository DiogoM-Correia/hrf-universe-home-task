According to my view, the next steps here could be: 
1) The SQL query could optimized if needed with indexes or even partitions if needed. 
It is also possible to make the calculation in python, by chunks divided standard job in order not to pull the full database to python but I beleive PostgreSQL is a good option for this case
2) The build logic should be validated to make sure we are deleting the correct cases with the percentils (maybe with specific cases)
3) At the moment we just have manual run with specific commands. This should be integrated in a pipeline to run everytime and the API should be automatically launched