# coding=utf-8

"""
   Copyright 2011-2016 STACKOPS TECHNOLOGIES S.L.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import requests
import json
import logging

logger_ = logging.getLogger(__name__)

class Zendesk:
    """Zendesk in the system"""

    username_ = None
    password_ = None
    url_ = None
    
    def __init__(self, url, username, password):
        self.url_ = url
        self.username_ = username
        self.password_ = password

    def createOrganization(self, organization):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        payload = {"organization": {"name": "%s"  % organization}}
        r = requests.post("%s/organizations.json" % (self.url_), auth=(self.username_, self.password_),
                          headers=headers, data=json.dumps(payload), verify=False)
        response = r.json()
        return response["organization"]["id"]

    def createUser(self, username, email, organization_id):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        payload = {"user": {"name": "%s" % username, "email": "%s" % email, "active": True, "verified": False, "organization_id": "%s" % organization_id}}
        r = requests.post("%s/users.json" % (self.url_), auth=(self.username_, self.password_), headers=headers,
                        data=json.dumps(payload), verify=False)
        response = r.json()
        return response["user"]["id"]
