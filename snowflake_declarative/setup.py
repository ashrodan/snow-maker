from setuptools import setup, find_packages

setup(
    name="snowflake-declarative",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "PyYAML>=5.1",
        "snowflake-core>=1.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A declarative framework for managing Snowflake resources",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/snowflake-declarative",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
