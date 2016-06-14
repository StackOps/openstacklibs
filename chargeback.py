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
import re

logger_ = logging.getLogger(__name__)

class Account:
    """Accounts in the system"""

    tenant_regexp_ = None
    token_ = None
    url_ = None
    
    def __init__(self, token, url, filter="^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$"):
        self.tenant_regexp_ = re.compile(filter)
        self.token_ = token
        self.url_ = url
        
    def getAll(self, status="CREATED"):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/account" % self.url_, headers=headers, verify=False)
        data = r.json()
        logger_.info("size=%s" % len(data["accounts"]))
        accounts = []
        for account in data["accounts"]:
            if account["status"] == status or status == "ALL":
                if self.tenant_regexp_.match(account["name"]):
                    accounts.append(account)
                    logger_.info("Account=%s" % account)
        return accounts

    def getAccountByName(self, name):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/account" % self.url_, headers=headers, verify=False)
        data = r.json()
        for account in data["accounts"]:
            if account["name"] == name:
                return account
        return None

    def getStatus(self, accountId):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/account/%s/status" % (self.url_, accountId), headers=headers, verify=False)
        data = r.json()
        return data

    def consumeInvoice(self, account_id, payment, description, transactionId, invoice_url):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        payload = {"transaction": {"amount": payment, "description": description, "transactionId": transactionId,
                                   "invoice": invoice_url}}
        r = requests.post("%s/api/account/%s/consume" % (self.url_, account_id), headers=headers, data=json.dumps(payload), verify=False)
        response = r.json()
        return response

    def getCurrent(self):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/account/current" % self.url_, headers=headers, verify=False)
        data = r.json()
        return data

    def getCurrentStatus(self):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/account/status" % (self.url_), headers=headers, verify=False)
        data = r.json()
        return data

    def update(self, account_id, account_json):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.put("%s/api/account/%s" % (self.url_, account_id), headers=headers, data=json.dumps(account_json), verify=False)
        data = r.json()
        return data

    def enterPromoCurrent(self, promo_code):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.post("%s/api/account/current/promo/%s" % (self.url_, promo_code), headers=headers, data=json.dumps({}), verify=False)
        data = r.json()
        return data

    def enterPromo(self, account_id, promo_code):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.post("%s/api/account/%s/promo/%s" % (self.url_, account_id, promo_code), headers=headers, data=json.dumps({}), verify=False)
        data = r.json()
        return data

class Cycle:
    """Cycle in the system"""
    
    token_ = None
    url_ = None
    
    def __init__(self, token, url):
        self.token_ = token
        self.url_ = url

    def getBillableAccounts(self):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/account" % self.url_, headers=headers)
        data = r.json()
        logger_.info("size=%s" % len(data["accounts"]))
        accounts = []
        for account in data["accounts"]:
	        if account["status"] == "ACTIVE" or account["status"] == "SUSPENDED":
	            accounts.append(account)
                logging.info("Account billable=%s" % account)
        return accounts

    def getBillableAccountCycle(self, account_id, invoice_range):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/account/%s/cycle" % (self.url_, account_id), headers=headers)
        data = r.json()
        cycles = data["cycles"]
        max_billing_cycle_id = 0
        for cycle in cycles:
            start = cycle["start"]
            end = cycle["end"]
            if invoice_range >= start and invoice_range <= end:
                if cycle["id"] > max_billing_cycle_id:
                    max_billing_cycle_id = cycle["id"]
        return max_billing_cycle_id


    def getCycle(self, cycle_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/cycle/%s" % (self.url_, cycle_id), headers=headers)
        data = r.json()
        return data

    def getProjects(self, cycle_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/cycle/%s/project" % (self.url_, cycle_id), headers=headers)
        data = r.json()
        return data

    def getProducts(self, project_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/api/project/%s/product" % (self.url_, project_id), headers=headers)
        data = r.json()
        return data
