"""Repository Utilitiles."""


from typing import Final


class AtCoderURLProvider:
    """URL情報を保持するクラス."""

    _atcoder_url: Final[str] = "https://atcoder.jp"
    login_url: Final[str] = f"{_atcoder_url}/login"

    @staticmethod
    def contest_url(contest: str) -> str:
        """contestのURLを返す.

        Args:
            contest (str):

        Returns:
            str:
        """
        return f"{AtCoderURLProvider._atcoder_url}/contests/{contest}"

    @staticmethod
    def task_url(contest: str, task: str) -> str:
        """taskのURLを返す.

        Args:
            contest (str):
            task (str):

        Returns:
            str:
        """
        return f"{AtCoderURLProvider.contest_url(contest)}/tasks/{contest}_{task}"

    @staticmethod
    def submit_url(contest: str) -> str:
        """submitのURLを返す.

        Args:
            contest (str):

        Returns:
            str:
        """
        return f"{AtCoderURLProvider.contest_url(contest)}/submit"
