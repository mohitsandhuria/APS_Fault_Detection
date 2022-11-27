from setuptools import find_packages,setup
from typing import List

REQUIREMENtS_FILE_NAME="requirements.txt"
HYPHEN_E_DOT="-e ."
def get_requirements()->List[str]:
    with open(REQUIREMENtS_FILE_NAME) as requirements_file:
        requirements_list=requirements_file.readlines()
        requirements_list=[requirements_name.replace("\n","") for requirements_name in requirements_list]
    if HYPHEN_E_DOT in requirements_list:
        requirements_list.remove(HYPHEN_E_DOT)
    return requirements_list

setup(
    name="sensor",
    version="0.0.1",
    author="ineuron",
    author_email="mohitsandhuria@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)