import os

class FileSystemReader:
  def __init__(self, input_directory, doc_search_pattern):
    self.input_directory = input_directory
    self.doc_search_pattern = doc_search_pattern

  def read(self):
    for file_path in self.get_all_file_paths(self.input_directory):
      with open(file_path, 'r') as file:
         yield file.read()

  def get_all_file_paths(self, directory):
    with os.scandir(directory) as entries:
      for entry in entries:
        if entry.is_file:
          yield entry.path
        elif entry.is_dir:
          for child in self.get_all_file_paths(entry.path):
            yield child
