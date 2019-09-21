import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
requires = [x.strip() for x in content] 

setuptools.setup(
    name="config_with_yaml",
    version="0.1.0",
    author="aitormf",
    author_email="aitor.martinez.fernandez@gmail.com",
    description="Loads configurations from yaml files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aitormf/config_with_yaml",
    install_requires=requires,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
