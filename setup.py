import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aio-oligo",
    version="0.1",
    author="Gorka Olalde Mendia",
    author_email="gorka.olalde@gmail.com",
    description="Asyncio version of the python-oligo library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olaldiko/aio-oligo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO"
    ],
    python_requires='>=3.6',
)

