from copyreg import pickle
from fileinput import filename
import sys
from pkg_resources import require
import requests
from textwrap import indent
from typing import List
import pickle
import os
from bs4 import BeautifulSoup

from atcoder_helper.models.test_case import TestCase


class AlreadyLoggedIn(Exception):
    pass


class AtCoderRepository:
    atcoder_url = "https://atcoder.jp"
    login_url = f"{atcoder_url}/login"

    def contest_url(self, contest: str) -> str:
        return f"{self.atcoder_url}/contests/{contest}"

    def task_url(self, contest: str, task: str) -> str:
        return f"{self.contest_url(contest)}/tasks/{contest}_{task}"

    def submit_url(self, contest: str) -> str:
        return f"{self.contest_url(contest)}/submit"

    def __init__(self, session_filename):
        self._session_filename = session_filename
        if os.path.isfile(session_filename):
            with open(session_filename, "rb") as file:
                self._session = pickle.load(file)
        else:
            self._session = requests.session()

    def write_session(self):
        with open(self._session_filename, "wb") as file:
            pickle.dump(self._session, file)

    def _get_csrf_token(self) -> str:
        login_page = self._session.get(self.login_url, cookies="")
        html = BeautifulSoup(login_page.text, "html.parser")

        token = html.find("input").attrs["value"]
        return token

    def login(self, username: str, password: str) -> bool:
        if self.is_logged_in():
            raise AlreadyLoggedIn("すでにloginしています")

        csrf_token = self._get_csrf_token()

        res = self._session.post(
            self.login_url,
            params={
                "username": username,
                "password": password,
                "csrf_token": csrf_token,
            },
            allow_redirects=0,
        )

        if res.headers["Location"] == "/home":
            self.write_session()
            return True
        else:
            return False

    def logout(self):
        self._session = requests.session()
        self.write_session()

    def is_logged_in(self) -> bool:
        # たたもさんの https://github.com/Tatamo/atcoder-cli/blob/0ca0d088f28783a4804ad90d89fc56eb7ddd6ef4/src/atcoder.ts#L46　を参考にしている

        res = self._session.get(self.submit_url("abc001"), allow_redirects=0)
        return res.status_code == 200  # login していなければ302 redirect になる

    def fetch_test_cases(self, contest: str, task: str) -> List[TestCase]:
        def normalize_newline(text: str) -> str:
            return "\n".join(text.splitlines())

        task_page = self._session.get(self.task_url(contest, task))
        html = BeautifulSoup(task_page.text, "html.parser")

        sections = (
            html.find("div", id="task-statement")
            .find("span", attrs={"class": "lang-ja"})
            .find_all("section")
        )

        input_sections = {
            section.find("h3").text.split()[1]: normalize_newline(
                section.find("pre").text
            )
            for section in sections
            if "入力例" in section.find("h3").text
        }

        output_sections = {
            section.find("h3").text.split()[1]: normalize_newline(
                section.find("pre").text
            )
            for section in sections
            if "出力例" in section.find("h3").text
        }

        return [
            TestCase(f"case-{name}", given, output_sections[name])
            for (name, given) in input_sections.items()
        ]


def main():
    args = sys.argv

    atcoder_repository = AtCoderRepository("session/session_dump.pkl")
    # test_cases = atcoder_repository.fetch_test_cases(args[1], args[2])

    return
    for case in test_cases:
        print(f"CASE-{case.name}")
        print("    input:")
        print(indent(case.given, "        "))
        print("    expected:")
        print(indent(case.expected, "        "))


if __name__ == "__main__":
    main()
