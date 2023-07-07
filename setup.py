from setuptools import setup, find_packages

setup(
    name="st-stripe",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "stripe",
        "httpx-oauth",
        "pyjwt"

    ],
    author="Tyler Richards",
    author_email="tylerjrichards@gmail.com",
    description="A Python package for creating subscription Streamlit apps",
    url="https://github.com/tylerjrichards/st-stripe",
)