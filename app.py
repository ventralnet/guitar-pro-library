import sqlite3
import click

from commands.create_database_command import CreateDatabaseCommand
from commands.drop_database_command import DropDatabaseCommand
from commands.build_database_command import BuildDatabaseCommand

@click.group()
@click.pass_context
@click.option(
  '-db',
  '--db-file', 
  required=False, 
  default='./tabs.db', 
  show_default=True, 
  help='Filename to store or location of existing database')
def cli(ctx, db_file):
  global connection
  ctx.obj['db_file'] = db_file


@cli.command('initialize-database', help='Initialize database if not exists. Use force to clear and rebuild database')
@click.pass_context
@click.option(
  '-f', 
  '--force',
  type=bool,
  required=False,
  default=False,
  is_flag=True,
  help='If database exists, delete all entries and recreate')
def initializeDatabase(ctx, force):
  ctx.obj['is_force'] = force
  print("db is {ctx.obj['db_file']}")
  with sqlite3.connect(ctx.obj['db_file']) as connection:
    ctx.obj['connection'] = connection
    if force:
      DropDatabaseCommand().execute(ctx.obj)
    CreateDatabaseCommand().execute(ctx.obj)

@cli.command('build-database', help='Rebuild database using tab locations passed')
@click.option("--input-path", "-i", multiple=True)
@click.pass_context
def buildDatabase(ctx, input_path):
  with sqlite3.connect(ctx.obj['db_file']) as connection:
    ctx.obj['connection'] = connection
    ctx.obj['tab_dirs'] = input_path
    BuildDatabaseCommand().execute(ctx.obj)

if __name__ == '__main__':
    cli(obj={})

