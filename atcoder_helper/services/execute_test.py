"""テストケース実行のためのメソッド."""

from textwrap import indent
from typing import List

from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.models.test_case import TestResult
from atcoder_helper.models.test_case import TestStatus
from atcoder_helper.repositories.test_case_repo import TestCaseRepository


def execute_test() -> None:
    """testcaseに基づき、テストを実行する関数."""
    test_case_repo = TestCaseRepository("testcases.yaml")

    test_cases = test_case_repo.read()
    results = _execute_and_show(test_cases)
    _show_summary(results)


def _execute_and_show(test_cases: List[AtcoderTestCase]) -> List[TestResult]:

    results = []
    for test_case in test_cases:
        print("-----------------------------------")
        result = test_case.execute()
        print(f"{test_case.name:<15}: {result.status.dyed}")
        results.append(result)

        if result.status == TestStatus.JUSTSHOW:
            print("    output:")
            print(indent(result.actual, "       >"))
        if result.status == TestStatus.ERROR:
            print(result.error)
        if result.status == TestStatus.WA:
            if result.expected is None:
                raise Exception("internal error")

            print("    expected:")
            print(indent(result.expected, "       >"))
            print("    but got:")
            print(indent(result.actual, "       >"))

    return results


def _show_summary(results: List[TestResult]) -> None:
    print("========================================")
    print("SUMMARY:")
    for result in results:
        print(f"{result.name:<15}: {result.status.dyed}")


if __name__ == "__main__":
    execute_test()
