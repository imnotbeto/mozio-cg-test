import os

# MOZIO
GET_MOZIO_URL = lambda: os.environ["MOZIO_URL"]
GET_MOZIO_AUTH_TOKEN = lambda: os.environ["MOZIO_AUTH_TOKEN"]
MAX_POLLS = 10

# Test Variables
DUMP_MOZIO_URL = "https://dump.mozio.com"
DUMP_AUTH_TOKEN = "dump-auth-token"
