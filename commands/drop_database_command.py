import click

from commands.base_command_interface import BaseCommandInterface
from commands.command_context_exception import CommandContextException

# relative_path, md5sum, meta_name, meta_artist, meta_album, meta_comments
DROP_TABLE = '''
  DROP TABLE IF EXISTS tabs
'''

class DropDatabaseCommand(BaseCommandInterface):
  def execute(self, context):
    connection = context['connection']
    if (not connection):
      raise CommandContextException("DropDatabaseCommand failed, no connection found on context")

    cursor = connection.cursor()
    cursor.execute(DROP_TABLE)
    