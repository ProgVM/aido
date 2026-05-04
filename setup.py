from setuptools import setup, find_packages

setup(
    name="aido",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "google-genai",
        "duckduckgo-search",
        "trafilatura",
    ],
    entry_points={
        "console_scripts": [
            "aido=aido.main:main",
        ],
    },
)
