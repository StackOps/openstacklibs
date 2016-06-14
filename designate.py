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


class Designate:
    """Designate in the system"""

    token_ = None
    url_ = None

    def __init__(self, token, url):
        self.token_ = token
        self.url_ = url

    def get_all_domains(self):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/domains" % (self.url_), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_records(self, domain_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/domains/%s/records" % (self.url_, domain_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def delete_domain(self, domain_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/domains/%s" % (self.url_, domain_id), headers=headers, verify=False)
        return r.status_code

    def delete_record(self, domain_id, record_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/domains/%s/records/%s" % (self.url_, domain_id, record_id), headers=headers, verify=False)
        return r.status_code


