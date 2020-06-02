from setuptools import setup

requirements = [
    "discord.py>=1.3.3",
    "textstat>=0.6.2",
    "inflect>=4.1"
]

setup(
    author="ibanner56",
    url="https://github.com/ibanner56/OtherDave",
    version="2.0.0",
    packages=["otherdave", "otherdave.commands", "otherdave.util"],
    license="MIT",
    description="OtherDave is not David.",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">3.5.3"
)