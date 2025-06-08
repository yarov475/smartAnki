from smartanki.configurator import setup_config_interactively


def handle_config(args):
    if args.config_command == "init":
        setup_config_interactively()
