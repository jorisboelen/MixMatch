import click
from alembic.command import upgrade
from alembic.config import Config
from argon2 import PasswordHasher
from mixmatch import __application__, __version__
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.tasks import task_cleanup, task_import
from os import path


@click.group()
@click.version_option(prog_name=__application__, version=__version__)
def main():
    pass


@main.command()
def migrate():
    config = Config(file_=path.join(path.dirname(__file__), "alembic.ini"))
    config.set_main_option("script_location", path.join(path.dirname(__file__), "alembic"))
    upgrade(config, "head")


@main.command()
def cleanup_covers():
    task_cleanup.delay()


@main.command()
def import_music():
    task_import.delay()


@main.command()
@click.argument("username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def reset_password(username, password):
    db = next(get_db())
    user = crud.get_user(db=db, username=username)
    crud.update_user_password(db=db, db_user=user, hashed_password=PasswordHasher().hash(password))
    click.echo("Password updated")


if __name__ == "__main__":
    main()
