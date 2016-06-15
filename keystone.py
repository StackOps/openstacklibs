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

class Keystone:
    """Keystone in the system"""

    token_ = None
    url_ = None
    username_ = None
    password_ = None
    tenant_ = None
    credentials_ = None
    tenantId_ = None
    
    def __init__(self, url, username, password, tenant, tenantid = None):
        self.url_ = url
        self.username_ = username
        self.password_ = password
        if tenantid is None:
            self.tenant_ = tenant
            credentials = json.dumps({"auth":{"passwordCredentials": {"username": "%s" % self.username_ , "password": "%s" % self.password_}, "tenantName": "%s" %  self.tenant_}})
        else:
            self.tenantId_ = tenantid
            credentials = json.dumps({"auth":{"passwordCredentials": {"username": "%s" % self.username_ , "password": "%s" % self.password_}, "tenantId": "%s" %  self.tenantId_}})
        headers = {"Content-Type": "application/json"}
        r = requests.post("%s/tokens" % self.url_, headers=headers, data=credentials, verify=False)
        if r.status_code==200:
            self.credentials_ = r.json()
            self.token_ = self.credentials_['access']['token']['id']
            self.tenantId_ = self.credentials_['access']['token']['tenant']['id']
            self.tenant_ = self.credentials_['access']['token']['tenant']['name']

    def getToken(self):
        if self.token_==None:
            return None
        return self.token_

    def getTenants(self):
        if self.token_==None:
            return []
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/tenants" % self.url_, headers=headers, verify=False)
        data = r.json()
        logger_.info("Tenants=%s" % len(data["tenants"]))
        return data

    def getTenant(self, os_tenant_name):
        if self.token_==None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/tenants" % self.url_, headers=headers, verify=False)
        data = r.json()
        if 'error' in data:
            raise Exception(data['error']['message'])
        tenants =  data['tenants']
        for tenant in tenants:
            tenant_name = tenant['name']
            if tenant_name == os_tenant_name:
                return tenant
        return None

    def getUsers(self):
        if self.token_==None:
            return []
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/users" % self.url_, headers=headers, verify=False)
        data = r.json()
        logger_.info("Users=%s" % len(data["users"]))
        return data

    def getTenantUsers(self):
        if self.token_==None:
            return []
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/tenants/%s/users" % (self.url_, self.tenantId_), headers=headers, verify=False)
        data = r.json()
        logger_.info("Users=%s" % len(data["users"]))
        return data

    def getRolesUser(self, userId):
        if self.token_==None:
            return []
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/tenants/%s/users/%s/roles" % (self.url_, self.tenantId_, userId), headers=headers, verify=False)
        data = r.json()
        logger_.info("Roles=%s" % len(data["roles"]))
        return data

    def getTenantUsersNonAdmin(self):
        if self.token_==None:
            return []
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/tenants/%s/users" % (self.url_, self.tenantId_), headers=headers, verify=False)
        data = r.json()
        logger_.info("Users=%s" % len(data["users"]))
        users = data["users"]
        usersNonAdmin = []
        for user in users:
            userId = user["id"]
            roles = self.getRolesUser(userId)
            addUser = True
            for role in roles["roles"]:
                roleName = role["name"]
                if roleName=="admin":
                    addUser = False
            if addUser:
                usersNonAdmin.append(user)
        return usersNonAdmin

    def getRolesUserAll(self, userId):
        if self.token_==None:
            return []
        tenants = self.getTenants()
        roles = []
        for t in tenants['tenants']:
            if t['enabled']:
                headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
                r = requests.get("%s/tenants/%s/users/%s/roles" % (self.url_, t['id'], userId), headers=headers, verify=False)
                data = r.json()
                rs = data["roles"]
                if len(rs)>0:
                    roles.append(rs)
        return roles

# Not working
    def getRolesUserAllGlobal(self, userId):
        if self.token_==None:
            return []
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/users/%s/roles" % (self.url_, userId), headers=headers, verify=False)
        data = r.json()
        logger_.info("Roles=%s" % len(data["roles"]))
        return data


    def update_tenant(self, tenant):
        if self.token_==None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.post("%s/tenants/%s" % (self.url_, tenant['id']), headers=headers,
                          data=json.dumps({"tenant": tenant}), verify=False)
        data = r.json()
        return data

    def remove_role_from_user(self, tenant_id, user_id, role_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/tenants/%s/users/%s/roles/OS-KSADM/%s" % (self.url_,  tenant_id, user_id, role_id), headers=headers, verify=False)
        return r.status_code

    def delete_tenant(self, tenant_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/tenants/%s" % (self.url_,  tenant_id), headers=headers, verify=False)
        return r.status_code

    def create_user(self, username, password, email, enabled=True):
        if self.token_==None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        payload = {
            "user": {
                "name": username,
                "email": email,
                "enabled": enabled,
                "OS-KSADM:password": password
            }
        }
        r = requests.post("%s/users" % self.url_, headers=headers, data=json.dumps(payload), verify=False)
        if r.status_code == 200:
            data = r.json()
            return data['user']
        raise Exception('HTTP Error:%s' % r.status_code)

    def grant_role_to_user(self, tenant_id, user_id, role_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.put("%s/tenants/%s/users/%s/roles/OS-KSADM/%s" % (self.url_,  tenant_id, user_id, role_id), headers=headers, verify=False)
        if r.status_code == 200:
            return
        raise Exception('HTTP Error:%s' % r.status_code)
