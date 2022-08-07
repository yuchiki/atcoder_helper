from typing import List

import yaml

from atcoder_helper.models.test_case import TestCase


class TestCaseRepository:
    def __init__(self, filename):
        self._filename = filename

    def write(self, test_cases: List[TestCase]):
        def str_presenter(dumper, data):
            if len(data.splitlines()) > 1:  # check for multiline string
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
            return dumper.represent_scalar("tag:yaml.org,2002:str", data)

        yaml.add_representer(str, str_presenter)

        with open(self._filename, "w") as file:
            yaml.dump(test_cases, file, sort_keys=False)

    def read(self) -> List[TestCase]:
        with open(self._filename) as file:
            objects = yaml.safe_load(file)
            return [TestCase.from_dict(object) for object in objects]
