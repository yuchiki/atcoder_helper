"""atcoder_helperコマンドのエントリポイント."""

from atcoder_helper.scripts.executor import Executor
from atcoder_helper.scripts.parser import get_root_parser


def main() -> None:
    """entrypoint."""
    executor = Executor()

    root_parser = get_root_parser()
    args = root_parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(self=executor, args=args)
    else:
        args.parser.print_help()
