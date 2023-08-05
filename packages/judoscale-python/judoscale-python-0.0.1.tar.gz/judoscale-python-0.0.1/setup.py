import setuptools

VERSION="0.0.1"
INSTALL_REQUIRES = ["requests<3.0.0"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="judoscale-python",
    version=VERSION,
    author="Adam McCrea",
    author_email="adam@adamlogic.com",
    description="Official Python adapter for Judoscale—the advanced autoscaler for Heroku",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/judoscale/judoscale-python",
    project_urls={
        "Issue Tracker": "https://github.com/judoscale/judoscale-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=INSTALL_REQUIRES,
)
