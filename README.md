# dnlab-challenge

Code challenge for web scraping and data extraction of the static website URparts, and also serving an API to request its data.

## Usage

Run the environment through docker-compose:

```bash
docker-compose up
```

It will build a MongoDB database, a FastAPI server and it will run the scraper in a container. It is important to run the scraper once (in an empty MongoDB collection) since the script does not deal with erasing the MongoDB collection in order to populate it.

Then, access the API server docs through:

```bash
http://localhost:8000/docs
```

Queries can be performed in order to filter the records:

```bash
http://localhost:8000/api/parts?model=ASC100
```

Tests can be done inside the API container through:

```bash
pytest
```

## Notes

1. Indexes were created for each data column in order to speed up the queries. 
2. HTTP requests for the scraping script were parallelized (joblib) considering 8 workers in order to speed up the web scraping and data extraction.
3. The scraper should be executed once since the script does not deal with erasing the MongoDB collection in order to populate it. In a **production environment** the easiest way would be overwriting all the collection (erasing its data and then inserting all records) since the website does not present a way to identify new or removed data and they also do not have any identification. If a specific model is added/removed from the middle of a category we could not identify it unless we would perform a checking loop, which would be costly. For this implementation, we could use a platform to schedule tasks such as Apache Airflow, and then running the scraper monthly for instance.
4. The implementation in a pipeline platform would also help indentifying changes in the HTML structure, which would break the execution of the scraper and then would send a notification to a developer to check and recode the scraper.
