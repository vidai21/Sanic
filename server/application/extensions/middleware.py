from application.server import app
from application.extensions.cors import add_cors_headers
from application.extensions.options import setup_options

app.register_listener(setup_options, "before_server_start")

# Fill in CORS headers
app.register_middleware(add_cors_headers, "response")