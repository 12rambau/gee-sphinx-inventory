"""All the process that can be run using nox.

The nox run are build in isolated environment that will be stored in .nox. to force the venv
update, remove the .nox/xxx folder.
"""

import nox

nox.options.sessions = ["lint", "mypy"]


@nox.session(reuse_venv=True)
def lint(session):
    """Apply the pre-commits."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(reuse_venv=True)
def mypy(session):
    """Run a mypy check of the lib."""
    session.install("mypy")
    test_files = session.posargs or ["inventory"]
    session.run("mypy", *test_files)


@nox.session(reuse_venv=True)
def generate(session):
    """Generate the inventory file."""
    session.install("-r", "./requirements.txt")
    session.run("python", "inventory/generate.py", silent=False)
