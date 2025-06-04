import warnings
from smartanki.parser.parser import parser_function
from smartanki.parser.task_switcher import task_switcher
warnings.filterwarnings("ignore", category=UserWarning)


def main():
    parser = parser_function()
    args = parser.parse_args()
    task_switcher(args)
if __name__ == "__main__":
    main()
