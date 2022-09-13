FROM python:3.10

RUN mkdir work
WORKDIR work

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY MANIFEST.in MANIFEST.in
COPY README.md README.md
COPY setup.py setup.py

COPY integration_test integration_test

COPY atcoder_helper atcoder_helper

RUN ls

RUN python setup.py sdist
RUN python setup.py bdist_wheel


RUN pip install dist/atcoder_helper-DUMMY-py3-none-any.whl
RUN which atcoder_helper
