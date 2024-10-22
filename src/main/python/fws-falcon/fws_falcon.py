#!/usr/bin/env -S poetry run python

import falcon
from fastwsgi import run

# Create a Falcon API instance
app = falcon.App()

class HelloWorld:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.media = {'Hello': 'World'}
        resp.status = falcon.HTTP_200  # HTTP Status 200 OK

# Add routes to the app
app.add_route('/', HelloWorld())

# Running the application with FastWSGI
if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8000)
