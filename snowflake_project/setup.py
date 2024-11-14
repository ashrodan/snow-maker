from setuptools import setup, find_packages

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='snowflake-connector',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A flexible Snowflake connection management library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/snowflake-connector',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'snowflake',
        'python-dotenv',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'snowflake-connector=main:main',
        ],
    },
    extras_require={
        'test': [
            'pytest',
            'mock',
        ],
    },
    keywords='snowflake database connector',
)
