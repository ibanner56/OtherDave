from setuptools import setup

requirements = [
    "discord.py>=1.3.3",
    "textstat>=0.6.2",
    "recognizers-text-number>=1.0.2a2"
]

setup(
    author="ibanner56",
    url="https://github.com/ibanner56/OtherDave",
    version="2.0.0",
    license="MIT",
    description="OtherDave is not David.",
    install_requires=requirements,
    python_requires=">3.5.3"
)