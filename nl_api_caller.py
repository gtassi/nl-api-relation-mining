import requests

class NlApiCaller:
  def __init__(self, token_url, api_url, username, password):
    self.api_url = api_url
    response = requests.post(
      token_url,
      json = { 'username': username, 'password': password }
    )
    self.authorization = 'Bearer ' + response.text

  def call(self, document):
    response = requests.post(
      self.api_url,
      headers = { 'Authorization': self.authorization },
      json = { 'document': { 'text': document } }
    )
    return response.json()
