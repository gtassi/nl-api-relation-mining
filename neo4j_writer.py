import requests
import base64
import re

class Neo4jWriter:
  def __init__(self, api_url, username, password):
    self.api_url = api_url
    self.authorization = 'Basic ' + base64.b64encode((username + ':' + password).encode('ascii')).decode('ascii')
    self.types_to_retrieve = re.compile('^[A-Z]+$')

  def write(self, api_output):
    for relation in api_output['data']['relations']:
      start_id = self.insert_or_retrieve(relation['verb'], False)
      self.write_related(relation, start_id)

  def write_related(self, object, start_id):
    for related in object['related']:
      end_id = self.insert_or_retrieve(related, True)
      requests.post(
        self.api_url,
        headers = { 'Authorization': self.authorization },
        json = {
          'statements': [{
            'statement': 'MATCH (start) MATCH (end) WHERE ID(start) = $start_id AND ID(end) = $end_id MERGE (start)-[r: ' + related['relation'] + ']->(end) RETURN ID(r)',
            'parameters': {
              'start_id': start_id,
              'end_id': end_id
            }
          }]
        }
      )
      if hasattr(related, 'related'):
        self.write_related(related, end_id)

  def insert_or_retrieve(self, object, reuse):
    node4j_statement = 'MERGE' if reuse and self.types_to_retrieve.match(object['type']) != None else 'CREATE'
    type = 'UNK' if object['type'] == '' else object['type']

    response = requests.post(
      self.api_url,
      headers = { 'Authorization': self.authorization },
      json = {
        'statements': [{
          'statement': node4j_statement + ' (x: ' + type + ' { lemma: $lemma }) RETURN ID(x)',
          'parameters': {
            'lemma': object['lemma']
          }
        }]
      }
    )

    return response.json()['results'][0]['data'][0]['row'][0]
