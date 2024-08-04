import click
import uvicorn
from alembic.command import upgrade
from alembic.config import Config
from argon2 import PasswordHasher
from mixmatch import __application__, __version__
from mixmatch.celery import celery
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.tasks import task_cleanup, task_import
from os import path


@click.group()
@click.version_option(prog_name=__application__, version=__version__)
def main():
    pass


@main.group()
def admin():
    pass


@admin.command()
def migrate():
    config = Config(file_=path.join(path.dirname(__file__), "alembic.ini"))
    config.set_main_option("script_location", path.join(path.dirname(__file__), "alembic"))
    upgrade(config, "head")


@admin.command()
@click.argument("username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def reset_password(username, password):
    db = next(get_db())
    user = crud.get_user(db=db, username=username)
    crud.update_user_password(db=db, db_user=user, hashed_password=PasswordHasher().hash(password))
    click.echo("Password updated")


@main.group()
def run():
    pass


@run.command()
@click.option('--host', default='127.0.0.1', show_default=True)
@click.option('--port', default=8000, show_default=True)
@click.option('--log-level', default="info", show_default=True,
              type=click.Choice(['critical', 'error', 'warning', 'info', 'debug', 'trace'], case_sensitive=False))
@click.option('--workers', default=10, show_default=True)
def server(host, port, log_level, workers):
    config = uvicorn.Config("mixmatch.app:app", host=host, port=port, log_level=log_level, workers=workers)
    server = uvicorn.Server(config)
    server.run()


@run.command()
@click.option('--log-level', default="INFO", show_default=True,
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'FATAL'], case_sensitive=False))
def scheduler(log_level):
    celery.start(argv=['beat', f'--loglevel={log_level}'])


@run.command()
@click.option('--log-level', default="INFO", show_default=True,
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'FATAL'], case_sensitive=False))
def worker(log_level):
    celery.worker_main(argv=['worker', f'--loglevel={log_level}'])


@main.group()
def task():
    pass


@task.command()
def cleanup_covers():
    task_cleanup.delay()


@task.command()
def import_music():
    task_import.delay()


if __name__ == "__main__":
    main()
