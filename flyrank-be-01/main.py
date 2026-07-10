from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FlyRank, this is Hassan's first endpoint!"}

@app.get("/status")
def read_status():
    return {"status": "Active", "intern": "Builder level - Ready for Backend AI"}