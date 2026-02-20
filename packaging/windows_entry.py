import os
from pathlib import Path
import uvicorn

from app.main import app


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
