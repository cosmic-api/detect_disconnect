# The core API class
from cosmic.api import API
# We use teleport to represent types
from teleport import Integer, String, Struct, required, optional

import os
from datetime import datetime, timedelta

# Name your API
api = API("detect_disconnect")

monitoring_items = {}

# Decorate your function with the parameter type and return type
@api.action(
  accepts=Struct([
        required("token", String),
        required("timeout", Integer),
        required("url", String)
    ])
)
def monitor(token, timeout, url):
  """
  If this endpoint is not called with identical token + url within
  timeout seconds, a GET request will be made to supplied url.

  If the token already exists and different URL is submitted, the call will fail. (exception)
  Timeout can be adjusted.

  The token will be cleared after the GET request is triggered.

  Max timeout is 60 seconds.
  """

  if timeout < 1 or timeout > 60:
    raise Exception("Timeout must be between [1 - 60] ")

  if token in monitoring_items:
    # Make sure URL is identical
    if monitoring_items[token][0] != url:
        raise Exception("Token is already in use.")

  # Update time with timeout setting.
  monitoring_items[token] = (url, datetime.now() + timedelta(seconds=timeout))

  print (token, timeout, url)
  
# Start running the api
if __name__ == "__main__":
  api.run(port=os.environ.get('PORT', 5100), debug=True)
