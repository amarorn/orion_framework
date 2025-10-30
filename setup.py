from setuptools import setup, find_packages

setup(
    name="orion-framework",
    version="0.1.0",
    description="Framework de engenharia de dados baseado em Clean Architecture",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.0.0",
        "pyyaml>=5.0",
        "click>=8.0",
    ],
    extras_require={
        "databricks": [
            "databricks-sql-connector>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "orion=application.cli.commands:cli",
        ],
    },
)

