"""テストケース実行のためのメソッド."""

import subprocess
from textwrap import indent
from typing import List

from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.models.test_case import TestResult
from atcoder_helper.models.test_case import TestStatus
from atcoder_helper.repositories.task_config_repo import TaskConfigRepository
from atcoder_helper.repositories.test_case_repo import TestCaseRepository


def execute_test() -> None:
    """testcaseに基づき、テストを実行する関数."""
    test_case_repo = TestCaseRepository("testcases.yaml")
    task_config_repo = TaskConfigRepository(".atcoder_helper_task_config.yaml")
    task_config = task_config_repo.read()

    subprocess.run(task_config.build)

    test_cases = test_case_repo.read()
    results = _execute_and_show(test_cases, task_config.run)
    _show_summary(results)


def _execute_and_show(
    test_cases: List[AtcoderTestCase], run_command: List[str]
) -> List[TestResult]:

    results = []
    for test_case in test_cases:
        print("-----------------------------------")
        result = test_case.execute(run_command)
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
