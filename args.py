import argparse


def load_args():
    """
    args parse_arges

    --headless: run in headless mode dest: headless
    """

    argument_parser = argparse.ArgumentParser(description="tiktok fire")
    argument_parser.add_argument(
        "--headless", action="store_true", help="Run in headless mode", dest="headless"
    )
    return argument_parser.parse_args()


if __name__ == "__main__":
    load_args()
