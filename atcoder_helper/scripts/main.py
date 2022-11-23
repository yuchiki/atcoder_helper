"""atcoder_helperコマンドのエントリポイント."""

from atcoder_helper.scripts.controller import get_default_controller
from atcoder_helper.scripts.parser import get_root_parser


def main() -> None:
    """entrypoint."""
    controller = get_default_controller()

    root_parser = get_root_parser()
    args = root_parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(self=controller, args=args)
    else:
        args.parser.print_help()
