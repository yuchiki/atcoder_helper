"""atcoder_helperコマンドのエントリポイント."""

from atcoder_helper.dependency import Dependency
from atcoder_helper.scripts.controller import Controller
from atcoder_helper.scripts.parser import get_root_parser


def main() -> None:
    """entrypoint."""
    injector = Dependency()
    controller = injector.resolve(Controller)

    root_parser = get_root_parser()
    args = root_parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(self=controller, args=args)
    else:
        args.parser.print_help()
