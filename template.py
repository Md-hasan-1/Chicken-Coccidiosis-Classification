import os
from pathlib import Path


path_list = [
    ".github/workflows/main.yaml",
    "config/config.yaml",
    "notebook/stage_01_data_ingestion.py",
    "notebook/stage_02_data_transformation.py",
    "notebook/stage_03_model_training.py",
    "notebook/stage_04_model_evaluation.py",
    "src/__init__.py",
    "src/components/__init__.py",
    "src/components/data/__init__.py",
    "src/components/data/ingestion.py",
    "src/components/data/transformation.py",
    "src/components/model/__init__.py",
    "src/components/model/training.py",
    "src/components/model/evaluation.py",
    "src/logger/__init__.py",
    "src/exception/__init__.py",
    "src/utils/__init__.py",
    "templates/index.html",
    "dvc.yaml",
    "requirements.txt",
    "setup.py",
    "README.md",
    ".gitignore",
    "pyproject.toml"
]

for filepath in path_list:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)):
        with open(filepath, "w") as f:
            pass

pyproject_data = """[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"
"""
with open("pyproject.toml", "wt") as file_obj:
    file_obj.write(pyproject_data)

with open(".gitignore", "a") as file_obj:
    file_obj.write("pyproject.toml\nnotebook/\nlogs/\n")

file_list = ["logger", "exception"]
for file_name in file_list:
    with open(Path(f"C:\Users\hasan\Documents\{file_name}.py"), "rt") as file:
        content = file.readlines()
    with open(Path(f"src/{file_name}/__init__.py", "w")) as file_obj:
        file_obj.writelines(content)

print("""
Task successfully completed. 👌
""")
