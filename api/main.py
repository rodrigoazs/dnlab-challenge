import uvicorn
import config
from fastapi import FastAPI
from routes import router


app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.VERSION,
    debug=config.DEBUG,
    openapi_tags=config.TAGS_METADATA
)

app.include_router(router, prefix=config.API_PREFIX)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
