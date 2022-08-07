import sys

from atcoder_helper.repositories.atcoder import AtCoderRepository
from atcoder_helper.repositories.test_case import TestCaseRepository


def fetch_task(contest: str, task: str):
    atcoder_repo = AtCoderRepository("session/session_dump.pkl")
    test_case_repo = TestCaseRepository("testcases.yaml")

    test_cases = atcoder_repo.fetch_test_cases(contest, task)

    test_case_repo.write(test_cases)


if __name__ == "__main__":
    fetch_task(sys.argv[1], sys.argv[2])
