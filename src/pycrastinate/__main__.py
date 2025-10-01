"""PyCrastinate CLI entry point."""

from pycrastinate.core import PyCrastinate


def main() -> None:
    """Run PyCrastinate CLI."""
    PyCrastinate().run_loop()

if __name__ == '__main__':
    main()

