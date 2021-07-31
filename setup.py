import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ohlclib",
    version="0.0.1",
    author="peterbill",
    author_email="peterbill.me@gmail.com",
    description="This project offers technical functions based on OHLC data for any time series price candle stick data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peterbillme/ohlclib",
    project_urls={
        "Bug Tracker": "https://github.com/peterbillme/ohlclib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
