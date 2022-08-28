"""Description of this package."""
import setuptools

from atcoder_helper._version import __version__

with open("README.md", "r") as readme:
    long_description = readme.read()

AUTHOR = "yuchiki"
EMAIL = "yuki.imai77@gmail.com"
URL = "https://github.com/yuchiki/atcoder_helper"


setuptools.setup(
    name="atcoder_helper",
    author=AUTHOR,
    author_email=EMAIL,
    package_data={"atcoder_helper": ["default_configs/*"]},
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    include_package_data=True,
    description="automation cli tools for AtCoder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT LICENSE",
    version=__version__,
    url=URL,
    download_url=URL,
    python_requires=">=3.10",
    install_requires=["colorama", "beautifulsoup4", "requests", "pyyaml", "pydantic"],
    entry_points={"console_scripts": "atcoder_helper=atcoder_helper.scripts.main:main"},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
