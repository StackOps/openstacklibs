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


class Cinder:
    """Cinder in the system"""

    token_ = None
    url_ = None

    def __init__(self, token, url):
        self.token_ = token
        self.url_ = url

    def get_all_volumes(self, tenant_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/%s/volumes" % (self.url_, tenant_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_snapshots(self, tenant_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/%s/snapshots" % (self.url_, tenant_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_global_volumes(self, tenant_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/%s/volumes/detail?all_tenants=1" % (self.url_, tenant_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def delete_volume(self, tenant_id, volume_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/%s/volumes/%s" % (self.url_, tenant_id, volume_id), headers=headers, verify=False)
        return r.status_code

    def set_volume_quotas(self, tenant_id, volumes, gigabytes, snapshots):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json", "Accept": "application/json"}
        payload = {
            "quota_set": {"volumes": 0, "gigabytes": 0, "snapshots": 0, "tenant_id": ""}}
        payload["quota_set"]["volumes"] = volumes
        payload["quota_set"]["gigabytes"] = gigabytes
        payload["quota_set"]["snapshots"] = snapshots
        payload["quota_set"]["tenant_id"] = tenant_id
        r = requests.put("%s/v1/%s/os-quota-sets/%s" % (self.url_, tenant_id, tenant_id), headers=headers,
                         data=json.dumps(payload), verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

