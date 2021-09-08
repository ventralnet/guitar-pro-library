import click

from commands.base_command_interface import BaseCommandInterface
from commands.command_context_exception import CommandContextException

# relative_path, md5sum, meta_name, meta_artist, meta_album, meta_comments
TAB_TABLE_SCHEMA = '''
  CREATE TABLE IF NOT EXISTS tabs (
    id INTEGER PRIMARY KEY,
    md5sum character(32) NOT NULL,
    meta_name varchar NULL,
    meta_artist varchar NULL,
    meta_album varchar NULL,
    meta_comments TEXT NULL
  )
'''

class CreateDatabaseCommand(BaseCommandInterface):
  def execute(self, context):
    connection = context['connection']
    if (not connection):
      raise CommandContextException("CreateDatabaseCommand failed, no connection found on context")

    cursor = connection.cursor()
    cursor.execute(TAB_TABLE_SCHEMA)
    