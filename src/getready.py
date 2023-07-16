from pathlib import Path
from urllib.error import HTTPError

from src.utils.text import compare_version, is_ver_str


def get():
    import httpx
    import wget
    import os
    import sys
    import logging
    import subprocess

    logging.info("Checking the ENV.")

    # Create the not exist folder.
    if not os.path.exists("reader"):
        os.mkdir("reader")

    if not os.path.exists("./reader/RKR"):
        os.mkdir("./reader/RKR")

    # Check reader.jar is exist or not.
    if not Path('./reader/reader.jar').exists():
        logging.warning("Reader not found.Try to download it from github.")

        # Get the latest version.
        latest = httpx.get("https://api.github.com/repos/hectorqin/reader/releases/latest").json()
        try:
            # Try to get the first `jar` file.
            # In default, the first `jar` file is the reader.jar.
            url = next(filter(lambda x: ".jar" in x["name"], latest["assets"]))["browser_download_url"]
        except (KeyError, StopIteration):
            logging.error(
                "Cannot get the reader file.Try to download it from rope("
                "https://github.com/hectorqin/reader/releases/latest).")
            sys.exit(0)

        try:
            # Try to download the reader.jar.
            wget.download(url, "./reader/reader.jar")
        except HTTPError:
            logging.warning("Cannot download the reader file.Try to download it from ghproxy.")
            try:
                # Try to download the reader.jar from ghproxy.
                wget.download(f"https://ghproxy.com/{url}", "./reader/reader.jar")
            except HTTPError:
                logging.error(f'Cannot download the reader file.Try to download it from {url}'
                              f' by yourself,then rename it as "reader.jar",put it into the reader folder.')
                sys.exit(0)
    try:
        # Run `java --version` to check the java version.
        output = subprocess.check_output(['java', '--version'], stderr=subprocess.STDOUT)
    except FileNotFoundError:
        logging.error('Java Not Found.Please Install Java 17+.You Can Download It From "https://adoptium.net"')
        sys.exit(0)

    # Get first line of the output.
    info_list = output.decode('utf-8').strip().split('\n').pop(0).split(' ')

    # Get first version string.
    version_str = next(filter(lambda x: is_ver_str(x), info_list))

    # Compare the version.
    if not compare_version(version_str, '17.0.0'):
        logging.error('Java version is too low.Please Install Java 17+.You Can Download It From "https://adoptium.net"')
        sys.exit(0)

    logging.info("Done.")


if __name__ == '__main__':
    ...
