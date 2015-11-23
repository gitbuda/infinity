# -*- coding: utf-8 -*-

import json
import falcon


class Resource:

    def on_get(self, req, resp):
        '''
        '''
        resp.status = falcon.HTTP_200  # This is the default status
        response = [{'description': 'database rest interface'}]
        resp.body = json.dumps(response)

app = falcon.API()
resource = Resource()
app.add_route('/api/description', resource)
