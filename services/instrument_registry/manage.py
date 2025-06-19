import os

import click
import pytest
import shutil

from instrument_registry.app.app import AppBuilder
from instrument_registry.app.extensions import db

app = AppBuilder().build()


@click.group()
def cli():
    pass


@cli.command()
def run():
    app.run()


@cli.command()
def test():
    exit(pytest.main(["tests"]))


@cli.command()
def clear_cache():
    for root, dirs, _ in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
    print("✅ Cleared __pycache__")


@cli.command()
def create_db():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    cli()
