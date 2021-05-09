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
