import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - [%(levelname)s] - %(message)s')

list_of_files = [
    "requirements.txt",
    "app.py",
    ".env",
    "src/helper.py",
    "src/prompt.py",
    "setup.py",
    "src/__init__.py",
    "experiments/experiment.ipynb"
]

for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir,file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir,exist_ok=True)
        logging.info(f"Creating directory: {file_dir} for the file {file_name}")

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path,"w") as f:
            logging.info(f"Creating empty file: {file_path}")
            pass
    else:
        logging.info(f"File already exists: {file_path}")
