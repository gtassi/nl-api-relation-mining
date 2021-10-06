import os
import json

from file_system_reader import FileSystemReader
from nl_api_caller import NlApiCaller
from neo4j_writer import Neo4jWriter

appsettings = json.load(open('appsettings.json', 'r'))

reader = FileSystemReader(appsettings['reader']['input_directory'], appsettings['reader']['doc_search_pattern'])
caller = NlApiCaller(appsettings['caller']['token_url'], appsettings['caller']['api_url'], appsettings['caller']['username'], appsettings['caller']['password'])
writer = Neo4jWriter(appsettings['writer']['api_url'], appsettings['writer']['username'], appsettings['writer']['password'])

for document in reader.read():
  api_output = caller.call(document)
  writer.write(api_output)
