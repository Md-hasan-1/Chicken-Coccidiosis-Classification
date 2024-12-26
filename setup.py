from setuptools import setup, find_packages
from typing import List

with open("README.md", "rt") as file_obj:
    long_description = file_obj.read()

project_name = "Chicken-Coccidiosis-Classification"

# This function gets all the names of packages 
def get_requirements(file:str)->List[str]:
    """
    params:
        - file -> path of file for requirements.
RETURNS: List of names present inside file obj.
    """
    requirements = list()
    HED = "-e ."
    with open(file) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HED in requirements:
            requirements.remove(HED)

    return requirements

setup(
    name=project_name,
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="markdown",
    author="Hasan Raza",
    author_email="hasanraza768001@gmail.com",
    url="https://github.com/Md-hasan-1/Chicken-Coccidiosis-Classification.git",
    package_dir= {"":"src"},
    packages=find_packages(where="src"),
    install_requires=get_requirements("requirements.txt")
)
