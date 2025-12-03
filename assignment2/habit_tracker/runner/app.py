import uvicorn
from fastapi import FastAPI

from ..infra.fastapi.api import router

app = FastAPI(title="Smart Habit Tracker API")

app.include_router(router)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
