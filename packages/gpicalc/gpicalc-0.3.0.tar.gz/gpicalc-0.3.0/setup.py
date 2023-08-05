import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gpicalc",
    version="0.3.0",
    author="M.Y. Chia",
    author_email="chiamy94@gmail.com",
    description="a package for calculating global performance indicator (GPI)",
    long_description_content_type="text/markdown",
    url="https://github.com/planta94/gpicalc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "gpicalc"},
    packages=setuptools.find_packages(where="gpicalc"),
    python_requires=">=3.6",
)