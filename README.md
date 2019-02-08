# OGCheckr: Steam Edition

Based on the popularity of [OGCheckr CLI](https://github.com/checker/cli) comes a newly improved and optimized command-line program made specifically for checking the availability of Steam community IDs and groups.

### Features

- Proxy support, use proxy lists (CSV only) from anywhere on your filesystem
- Use word lists (TXT) from anywhere on your filesystem.
- Multi-threaded for fast execution

## Installation

The installation process has been dramatically simplified from its predecessor. Simply install `Python 3.7+` and then run the following command in Terminal (macOS) or Command Prompt (Windows).

_Note:_ You will need to make sure Python is added to your system's environment variables. When running the installer, there is a checkbox under Advanced that can do this for you.

```bash
python3 -m pip install steamcheck
```

https://pypi.org/project/steamcheck

If not using pip, you can run the following command.

```
cd PATH && python3 setup.py install
```

_Note:_ Replace PATH with the full, absolute path of the extracted zip you downloaded.

## Usage

Unlike this program's predecessor, **OGCheckr Steam Edition** does not have a configuration file. You supply command-line arguments instead.
To see a listing of all the possible flags, type `steamcheck -h` anywhere in your shell of choice. No longer does the command need to be prefixed with "python".



##### Support & Feedback

If you find a bug in the program, please [file an issue](https://github.com/checker/steamcheck/issues).

If you need help with installation or usage, feel free to join the CrocBuzz Studios [Discord community](https://discord.gg/hpbQayV).

