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


class Swift:
    """Swift in the system"""

    tenant_regexp_ = None
    token_ = None
    url_ = None

    def __init__(self, token, url):
        self.token_ = token
        self.url_ = url

    def get_containers(self, token, tenant_id):
        headers = {"X-Auth-Token": "%s" % token, "Content-Type": "application/json"}
        r = requests.get("%s%s?format=json" % (self.url_, tenant_id), headers=headers, verify=False)
        if (r.status_code == 200):
            data = r.json()
        else:
            data = ""
        return data

    def set_quota_global(self, token, tenant_id, quota_bytes):
        headers = {"X-Auth-Token": "%s" % token, "Content-Type": "application/json",
                   "x-account-meta-quota-bytes": quota_bytes}
        r = requests.post("%s%s" % (self.url_, tenant_id), headers=headers, verify=False)
        return r.status_code

    def reset_quota_global(self, token, tenant_id):
        headers = {"X-Auth-Token": "%s" % token, "Content-Type": "application/json",
                   "x-account-meta-quota-bytes": ""}
        r = requests.post("%s%s" % (self.url_, tenant_id), headers=headers, verify=False)
        return r.status_code

    def create_container(self, token, tenant_id, container_name):
        headers = {"X-Auth-Token": "%s" % token, "Content-Type": "application/json"}
        r = requests.put("%s%s/%s" % (self.url_, tenant_id, container_name), headers=headers, verify=False)
        return r.status_code

    def set_quota_container(self, token, tenant_id, container_name, quota_bytes):
        headers = {"X-Auth-Token": "%s" % token, "Content-Type": "application/json",
                   "x-container-meta-quota-bytes": quota_bytes}
        r = requests.post("%s%s/%s" % (self.url_, tenant_id, container_name), headers=headers, verify=False)
        return r.status_code

    def reset_quota_container(self, token, tenant_id, container_name):
        headers = {"X-Auth-Token": "%s" % token, "Content-Type": "application/json",
                   "x-container-meta-quota-bytes": ""}
        r = requests.post("%s%s/%s" % (self.url_, tenant_id, container_name), headers=headers, verify=False)
        return r.status_code
