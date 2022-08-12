"""Description of this package."""
import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="atcoder_helper",
    version="0.0.0",
    install_requires=["colorama", "beautifulsoup4", "requests", "pyyaml"],
    entry_points={"console_scripts": "atcoder_helper=atcoder_helper.scripts.main:main"},
    author="Yuchiki",
    author_email="yuki.imai77@gmail.com",
    description="automation cli tools for AtCoder",
    long_description=long_description,
    long_description_content_type="test/markdown",
    url="https://github.com/yuchiki/atcoder_helper",
    packages=setuptools.find_packages(),
    classfiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
