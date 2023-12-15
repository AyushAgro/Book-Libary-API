from setuptools import find_packages
from setuptools import setup


VERSION = '1.0.0'
DESCRIPTION = 'Toptal Books Library API Python Package'
LONG_DESCRIPTION = 'Python Egg of book library api '

# Setting up
setup(
    name="books_library_api",
    version=VERSION,
    author="Shriyansh Agrawal",
    author_email="shriyansh@shellx.net",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=['python', 'toptal', 'Books Library API', 'RestFul'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ])
