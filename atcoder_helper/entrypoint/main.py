"""atcoder_helperコマンドのエントリポイント."""

from atcoder_helper.adapter.controller.controller import Controller
from atcoder_helper.adapter.controller.parser import get_root_parser
from atcoder_helper.dependency import Dependency


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
