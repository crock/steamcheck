import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fh:
    source_license = fh.read()

setuptools.setup(
    name="steamcheck",
    version="1.0.0",
    author="CrocBuzz Studios",
    author_email="alex@crocbuzzstudios.com",
    description="A command-line tool to check availability of lists of potential Steam IDs and Steam Groups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/checker/steamcheck",
    packages=setuptools.find_packages(),
    package_dir={'steamcheck': 'steamcheck'},
    python_requires=">=3.7",
    license=source_license,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['steamcheck=steamcheck.main:main'],
    }
)