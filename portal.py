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

class Portal:
    """Portal in the system"""

    url_ = None
    
    def __init__(self, url):
        self.url_ = url

    def register(self, username, email):
        headers = {"Content-Type": "application/json"}
        payload = {
            "register": {
                "username": username,
                "email": email
                }
            }
        r = requests.post("%s/api/register" % self.url_, headers=headers, data=json.dumps(payload), verify=False)
        if r.status_code == 200:
            data = r.json()
            return data
        raise Exception('HTTP Error:%s' % r.status_code)

    def fake_login(self, username, password, cloud):
        postFields = {
            'user': username,
            'password': password,
            'cloud': cloud}
        r = requests.post("%s/api/login" % self.url_, data=postFields, verify=False)
        if r.status_code == 200:
            return
        raise Exception('HTTP Error:%s' % r.status_code)
