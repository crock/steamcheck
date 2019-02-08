#!/usr/bin/env python3
import platform
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from steamcheck.check import Checker

module_name = "OGCheckr: Steam Edition"
__version__ = "1.0.0"

def main():
    version_string = f"{module_name}\n" + \
                     f"Version: {__version__}\n" + \
                     f"Python:  {platform.python_version()}"

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{module_name} (Version {__version__})"
                            )
    parser.add_argument("--version",
                        action="version", version=version_string,
                        help="Display version information and dependencies."
                        )
    parser.add_argument("--output", "-o", dest="output",
                        help="Path with filename to save results to. File does not have to exist. It will be generated automatically."
                        )
    parser.add_argument("--proxy_list", "-pl", metavar='PROXY_LIST',
                        action="store", dest="proxy_list", default=None,
                        help="Make requests over a proxy randomly chosen from a list generated from a .csv file."
                        )
    parser.add_argument("--word_list", "-wl", metavar='WORD_LIST',
                        action="store", dest="word_list", default=None,
                        help="Make requests over a proxy randomly chosen from a list generated from a .txt file."
                        )
    parser.add_argument("--check_proxies", "-cp", metavar='CHECK_PROXY',
                        action="store", dest="check_proxy", default=False,
                        help="To be used with the '--proxy_list' parameter. "
                             "The script will check if the proxies supplied in the .csv file are working and anonymous."
                        )
    parser.add_argument("--thread_count", "-tc", metavar='THREAD_COUNT',
                        action="store", dest="thread_count", default=1,
                        help="Specify the number of processor threads you want to use. Default is single-threaded (1)."
                        )

    args = parser.parse_args()
    checker = Checker(args)


if __name__ == "__main__":
    main()