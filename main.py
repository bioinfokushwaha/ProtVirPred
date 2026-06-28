import argparse
import os
import subprocess
import sys
from pathlib import Path
from fastapi import FastAPI


PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
app = FastAPI(root_path="/ParaVirPred")

@app.get("/")
def read_root():
    return {"message": "This is now running under /ParaVirPred"}

def build_frontend(skip_build: bool):

    dist_dir = FRONTEND_DIR / "dist"

    if skip_build:

        if not dist_dir.exists():

            print(
                "Warning: frontend/dist was not found. "
                "Run without --skip-frontend-build to build it."
            )

        return

    npm_command = "npm.cmd" if os.name == "nt" else "npm"

    print("\nBuilding frontend...")

    subprocess.run(
        [
            npm_command,
            "run",
            "build"
        ],
        cwd=FRONTEND_DIR,
        check=True
    )


def parse_args():

    parser = argparse.ArgumentParser(
        description="Run ParaVirPred frontend and backend from one process"
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host IP address"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Port number"
    )

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Reload backend on Python changes"
    )

    parser.add_argument(
        "--skip-frontend-build",
        action="store_true",
        help="Use the existing frontend/dist build"
    )

    return parser.parse_args()


def main():

    args = parse_args()

    build_frontend(args.skip_frontend_build)

    os.chdir(BACKEND_DIR)
    sys.path.insert(0, str(BACKEND_DIR))

    from app.server import app

    app.run(
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":

    main()
