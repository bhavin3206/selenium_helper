from setuptools import setup, find_packages

setup(
    name="selenium_helper",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "selenium"
    ],
    author="Bhavin Patel",
    author_email="bhavinpatel99987@gmail.com",
    description="A helper utility for Selenium WebDriver automation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bhavin3206/selenium_helper",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
