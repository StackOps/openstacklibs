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


class Nova:
    """Nova in the system"""

    token_ = None
    url_ = None

    def __init__(self, token, url):
        self.token_ = token
        self.url_ = url

    def get_all_vms(self, tenant_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/%s/servers/detail" % (self.url_, tenant_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_global_vms(self, tenant_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/%s/servers/detail?all_tenants=1" % (self.url_, tenant_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def delete_vm(self, tenant_id, vm_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/%s/servers/%s" % (self.url_, tenant_id, vm_id), headers=headers, verify=False)
        return r.status_code

    def get_all_floatings(self, floating_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/%s/os-floating-ips" % (self.url_, floating_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def delete_floating(self, tenant_id, floating_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/%s/os-floating-ips/%s" % (self.url_, tenant_id, floating_id), headers=headers, verify=False)
        return r.status_code

    def get_all_secgroups(self, secgroup_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/%s/os-security-groups" % (self.url_, secgroup_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def delete_secgroup(self, tenant_id, secgroup_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/%s/os-security-groups/%s" % (self.url_, tenant_id, secgroup_id), headers=headers, verify=False)
        return r.status_code

    def get_all_keypairs(self, keypair_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/%s/os-keypairs" % (self.url_, keypair_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def delete_keypair(self, tenant_id, keypair_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/%s/os-keypairs/%s" % (self.url_, tenant_id, keypair_id), headers=headers, verify=False)
        return r.status_code

    def set_compute_quotas(self, tenant_id, cores, ram, instances, key_pairs, security_group,
                           security_group_rules, floating_ips, metadata_items, injected_files):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json", "Accept": "application/json"}
        payload = {
            "quota_set": {"ram": 0, "key_pairs": 0, "instances": 0,
                          "security_group_rules": 0, "security_groups": 0,
                          "tenant_id": "", "floating_ips": 0, "cores": 0}}
        payload["quota_set"]["ram"] = ram
        payload["quota_set"]["key_pairs"] = key_pairs
        payload["quota_set"]["instances"] = instances
        payload["quota_set"]["security_groups"] = security_group
        payload["quota_set"]["security_group_rules"] = security_group_rules
        payload["quota_set"]["tenant_id"] = tenant_id
        payload["quota_set"]["floating_ips"] = floating_ips
        payload["quota_set"]["cores"] = cores
        payload["quota_set"]["metadata_items"] = metadata_items
        payload["quota_set"]["injected_files"] = injected_files
        r = requests.put("%s/v1.1/%s/os-quota-sets/%s" % (self.url_, tenant_id, tenant_id), headers=headers,
                         data=json.dumps(payload), verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

