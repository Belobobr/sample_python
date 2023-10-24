# Backend

## Getting started

1. Prerequisites

- [Python 3.7+](https://www.python.org/)
- Optional: [make](https://www.gnu.org/software/make/)

2. Create a virtual environment
   ```bash
   python3 -m venv .venv
   ```
3. Activate the virtual environment

   | Platform | Shell      | Command to activate virtual environment |
   | -------- | ---------- | --------------------------------------- |
   | POSIX    | bash/zsh   | $ source .venv/bin/activate             |
   | POSIX    | fish       | $ source .venv/bin/activate.fish        |
   | POSIX    | csh/tcsh   | $ source .venv/bin/activate.csh         |
   | Windows  | cmd.exe    | C:\> .venv\Scripts\activate.bat         |
   | Windows  | PowerShell | PS C:\> .venv\Scripts\Activate.ps1      |

   ([Reference](https://docs.python.org/3/library/venv.html#how-venvs-work))

   An example with bash:

   ```bash
   source .venv/bin/activate
   ```

4. Install depedencies
   ```bash
   pip3 install -r requirements.txt
   ```

## How to develop

For convenience, you can use `make <target>` if you have `make` available on your system:

```bash
$ make
Please use 'make <target>' where <target> is one of

  run-server     Start local API server
  test           Run tests
  static-checks  Run static checks
  reformat       Reformat code
  clean          Clean up all generated files
  install-deps   (Re)install dependencies

```

All the functionality can also be invoked by running the Python CLI directly:

- Start local API server: `python3 -m uvicorn src.server:app`
- Run tests with [pytest](https://docs.pytest.org/en/7.3.x/): `python3 -m pytest`
- Run static checks:
  - Run [pylint](https://pypi.org/project/pylint/): `python3 -m pylint src --rcfile pylint.rc`
  - Run [flake8](https://flake8.pycqa.org/en/latest/): `python3 -m flake8 src`
  - Run [black](https://github.com/psf/black): `python3 -m black src --check`
- Reformat code: `python3 -m black src`
- Install dependencies: `pip3 install -r requirements.txt`
