import setuptools

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hextech",
    version="1.0.12",
    author="bujustin",
    author_email="bujustin@gmail.com",
    description="A Python framework for accessing League of Legends esports data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bujustin/hextech",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
