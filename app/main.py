from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI Systems Engineer API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
