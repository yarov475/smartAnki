from smartanki.parser.admin_cli import handle_admin
from smartanki.parser.config_cli import handle_config
from smartanki.parser.review import run_review_session
from smartanki.parser.run_CLI import handle_run
from smartanki.parser.writing_cli import handle_writing


def task_switcher(args):
    if args.command == "run":
        handle_run(args)
    elif args.command == "admin":
        handle_admin(args)
    elif args.command == "review":
        run_review_session()
    elif args.command == "config":
        handle_config(args)
    elif args.command == "writing":
        handle_writing(args)
