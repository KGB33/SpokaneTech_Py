from typing import Callable
from asyncio import TaskGroup

import dagger
from dagger import dag, function

PYTHON_VERSION = "3.11-slim-bullseye"
GUNICORN_CMD = ["gunicorn", "--chdir", "./src", "--bind", ":8000", "--workers", "2", "spokanetech.wsgi"]


def base_container() -> dagger.Container:
    """
    Builds the base container from the `python:PYTHON_VERSION` docker image.
    """
    return (
        dag.container()
        .from_(f"python:{PYTHON_VERSION}")
        .with_exec(["pip", "install", "--upgrade", "pip"])
        .with_env_variable("PYTHONDONTWRITEBYTECODE", "1")
        .with_env_variable("PYTHONUNBUFFERED", "1")
        .with_exposed_port(8000)
    )


def requirements(requirements: dagger.File) -> Callable:
    """
    Used to install the provided requirements.txt in a container.

    >>> ctr.with_(requirements(requirements_file))
    """

    def _requirements(ctr: dagger.Container) -> dagger.Container:
        return (
            ctr.with_file("/tmp/requirements.txt", requirements)
            .with_exec(["pip", "install", "-r", "/tmp/requirements.txt"])
            .with_exec(["rm", "-rf", "/root/.cache/"])
        )

    return _requirements


def source(dir: dagger.Directory) -> Callable:
    """
    Adds the source directiory to a contianer and changes the workdir to that directory.

    >>> ctr.with_(source(some_dir))
    """

    def _source(ctr: dagger.Container) -> dagger.Container:
        return ctr.with_directory("/code", dir).with_workdir("/code")

    return _source


@function
def debug(dir: dagger.Directory) -> dagger.Container:
    """
    Builds a container without starting the web server for debugging.

    Use `dagger -m ci call debug --dir ./ shell` to open a terminal
    in the container.
    """
    return (
        base_container()
        .with_(requirements(dir.file("requirements.txt")))
        .with_(source(dir))
        .with_env_variable("SPOKANE_TECH_DEV", "true")
        .with_exec(["python", "src/manage.py", "migrate"])
    )


@function
async def lint(dir: dagger.Directory) -> str:
    """
    Checks that the directory passes various linters,
    i.e. `ruff check` and `ruff format`
    """
    ctr = base_container().with_(source(dir)).with_exec(["pip", "install", "ruff"])
    async with TaskGroup() as tg:
        fmt = tg.create_task(ctr.with_exec(["ruff", "format", "--check"]).stdout())
        chk = tg.create_task(ctr.with_exec(["ruff", "check"]).stdout())
    return f"{fmt.result()}\n\n{chk.result()}"


@function
async def bandit(dir: dagger.Directory) -> str:
    """
    Runs bandit on the provided directory.
    """
    return await (
        base_container()
        .with_(source(dir))
        .with_exec(["pip", "install", "bandit"])
        .with_exec(["bandit", "-c", "pyproject.toml", "-r", "src"])
        .stdout()
    )


@function
def local(dir: dagger.Directory) -> dagger.Service:
    """
    Used to run the website in a production **like** environment.

    `dagger -m ci --focus=false call local --dir ./ up --native`
    """
    return debug(dir).with_exec(GUNICORN_CMD).as_service()


@function
def prod(dir: dagger.Directory) -> dagger.Container:
    """
    Builds a production-ready container.
    """
    return base_container().with_(requirements(dir.file("requirements.txt"))).with_(source(dir)).with_exec(GUNICORN_CMD)
