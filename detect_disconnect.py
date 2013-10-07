# The core API class
from cosmic.api import API
# We use teleport to represent types
from teleport import Integer

import os

# Name your API
api = API("detect_disconnect")

# Decorate your function with the parameter type and return type
@api.action(
  accepts=Integer,
  returns=Integer
)
def monitor(number):
  """Start monitoring this request."""
  return number + 5
  
# Start running the api
if __name__ == "__main__":
  api.run(port=os.environ.get('PORT', 5100))
