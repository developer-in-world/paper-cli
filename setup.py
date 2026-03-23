from setuptools import setup, find_packages

setup(
    name="paper-cli",
    version="0.1.0",
    description="ML Paper to Code CLI Tool",
    author="Developer",
    packages=find_packages(),
    py_modules=["main", "fetcher", "code_finder", "summarizer", "config", "storage"],
    install_requires=[
        "requests",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "paper-cli=main:main",
        ],
    },
    python_requires=">=3.8",
)
