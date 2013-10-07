# The core API class
from cosmic.api import API
# We use teleport to represent types
from teleport import Integer, String, Struct, required

import os
from datetime import datetime, timedelta
import time

from multiprocessing import Process, Manager

import requests

def make_request(monitoring_items):
    """
    Make requets in really really simple ways.

    Should be deligated to separate workers.
    """
    while True:
        time.sleep(0.1)

        if len(monitoring_items) <= 0:
            continue

        urls = []

        # Get list of jobs to be triggered
        for token, value in monitoring_items.items():
            if value[1] < datetime.now():
                urls.append((token, value[0]))

        # Remove jobs which will be triggered
        for token, _ in urls:
            del monitoring_items[token]

        # make requests
        for token, url in urls:

            try:
                r = requests.get(url)
                print (token, r.url, r.status_code)
            except Exception as e:
                print e

# Name your API
api = API("detect_disconnect")

manager = Manager()
monitoring_items = manager.dict()

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

  Timeout of 0 will remove the item.
  """

  if timeout > 60:
    raise Exception("Timeout must be between [0 - 60]")

  if token in monitoring_items:
    # Make sure URL is identical
    if monitoring_items[token][0] != url:
        raise Exception("Token is already in use.")

  if timeout == 0 and token in monitoring_items:
    del monitoring_items[token]
  elif timeout > 0:
    # Update time with timeout setting.
    monitoring_items[token] = (url, datetime.now() + timedelta(seconds=timeout))


# Start running the api
if __name__ == "__main__":
    p = Process(target=make_request, args=(monitoring_items,))
    p.start()
    api.run(port=os.environ.get('PORT', 5100), debug=False)
