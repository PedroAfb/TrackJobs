from fastapi import FastAPI

from trackJobs.api.router import candidaturas

app = FastAPI(
    title="TrackJobs API",
    description="API para gerenciamento de candidaturas de empregos",
    version="1.0.0",
)

app.include_router(candidaturas.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
