import unittest
from unittest.mock import Mock

from commands.create_database_command import CreateDatabaseCommand, TAB_TABLE_SCHEMA
from commands.command_context_exception import CommandContextException
class TestCreateDatabaseCommand(unittest.TestCase):
  def setUp(self) -> None:
    self.command = CreateDatabaseCommand()
    
    mock_context = Mock()
    mock_context.connection = Mock()
    mock_context.connection.cursor.return_value = Mock()

    self.mock_context = mock_context
    
  def test_exception_if_no_connect_on_context(self):
    mock_context = Mock()
    mock_context.connection = None
    with self.assertRaises(CommandContextException):
      self.command.execute(mock_context)
  
  def test_create_table(self):
    self.command.execute(self.mock_context)

    self.mock_context.connection.cursor.assert_called_once()
    self.mock_context.connection.cursor().execute.assert_called_once_with(TAB_TABLE_SCHEMA)