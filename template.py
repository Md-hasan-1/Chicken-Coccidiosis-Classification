import os
from pathlib import Path


path_list = [
    ".github/workflows/main.yaml",
    "config/config.yaml",
    "notebook/stage_01_data_ingestion.ipynb",
    "src/__init__.py",
    "src/components/__init__.py",
    "src/pipeline/__init__.py",
    "src/configuration/__init__.py",
    "src/logger/__init__.py",
    "src/exception/__init__.py",
    "src/utils/__init__.py",
    "templates/index.html",
    "dvc.yaml",
    "requirements.txt",
    "setup.py",
    "app.py",
    "main.py",
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

# content for pyproject.toml
with open("pyproject.toml", "wt") as file_obj:
    file_obj.write(pyproject_data)

# content for .gitignore
with open(".gitignore", "a") as file_obj:
    file_obj.write("pyproject.toml\nnotebook/\nlogs/\nartifacts/\n")

# content for requirements.txt
with open("requirements.txt", "w") as file_obj:
    file_obj.write("mlflow\ndvc\nbentoml\nipykernel")

try:
    file_list = ["logger", "exception", "setup.py"]
    for file_name in file_list:
        with open(f"C:/Users/hasan/Documents/{file_name}.py", "rt") as file:
            content = file.readlines()
        with open(f"src/{file_name}/__init__.py", "w") as file_obj:
            file_obj.writelines(content)
    print("""
          Task successfully completed. 👌
          """)
except:
    string = "Unable to write files please write manually."
    skull = "💀"
    print(f"\n{skull*len(string)}\n{string}\n{skull*len(string)}\n")

print("""
-----------------X-----------------
""")
