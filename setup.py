import json
from setuptools import setup

with open("./requirements.txt") as rf:
    requirements = json.load(rf)

setup(
    author="ibanner56",
    url="https://github.com/ibanner56/OtherDave",
    version="2.0.0",
    packages=["otherdave", "otherdave.commands", "otherdave.util"],
    test_suite="test",
    license="MIT",
    description="OtherDave is not David.",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">3.5.3"
)