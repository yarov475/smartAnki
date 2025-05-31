from smartanki.admin_cli import handle_admin
from smartanki.config_cli import handle_config
from smartanki.review import run_review_session
from smartanki.run_CLI import handle_run


def task_switcher(args):
    if args.command == "run":
        handle_run(args)
    elif args.command == "admin":
        handle_admin(args)
    elif args.command == "review":
        run_review_session()
    elif args.command == "config":
        handle_config(args)
