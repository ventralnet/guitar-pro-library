from genericpath import isfile
import os
from glob import iglob
from hashlib import md5
import traceback

import progressbar

from commands.base_command_interface import BaseCommandInterface
from commands.command_context_exception import CommandContextException
from PyTabParser import PowerTab, Guitarpro3Tab, TabException

class BuildDatabaseCommand(BaseCommandInterface):

  SUPPORTED_FILE_TYPES = ['.gp5', '.gp4', '.gp3', '.gp2', 'gp1', 'gpx', '.gp']

  def execute(self, context):
    connection = context['connection']
    file_paths = context['tab_dirs']
    if (not connection):
      raise CommandContextException("CreateDatabaseCommand failed, no connection found on context")
    
    tab_files = self.parse_dirs(file_paths)
    self.processTabs(tab_files)

  def parse_dirs(self, file_paths):
    file_set = set()
    for path in file_paths:
      file_list = [f for f in iglob(f"{path}/**/*", recursive=True) if os.path.isfile(f) and os.path.splitext(f)[-1].lower() in self.SUPPORTED_FILE_TYPES]
      file_set.update(file_list)
    return file_set

  def processTabs(self, tab_files):
    for tab_file in progressbar.progressbar(tab_files):
      with open(tab_file, "rb") as file:
        hash = md5(file.read()).hexdigest().lower()
        try:
          tab = Guitarpro3Tab(tab_file)
        except TabException as error:
          traceback.print_exc()
        except Exception as error:
          raise(error) 

