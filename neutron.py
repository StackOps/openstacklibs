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


class Neutron:
    """Neutron in the system"""

    token_ = None
    url_ = None

    def __init__(self, token, url):
        self.token_ = token
        self.url_ = url

    def get_all_networks(self):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/networks.json" % self.url_, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_owned_networks(self, tenant_id):
        networks = self.get_all_networks()
        owned_networks = []
        if networks is not None:
            for network in networks['networks']:
                if network['tenant_id'] == tenant_id:
                    owned_networks.append(network)
        return {"networks": owned_networks}

    def get_all_subnets(self):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/subnets.json" % self.url_, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_owned_subnets(self, tenant_id):
        subnets = self.get_all_subnets()
        owned_subnets = []
        if subnets is not None:
            for subnet in subnets['subnets']:
                if subnet['tenant_id'] == tenant_id:
                    owned_subnets.append(subnet)
        return {"subnets": owned_subnets}

    def get_all_routers(self):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/routers.json" % self.url_, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_owned_routers(self, tenant_id):
        routers = self.get_all_routers()
        owned_routers = []
        if routers is not None:
            for router in routers['routers']:
                if router['tenant_id'] == tenant_id:
                    owned_routers.append(router)
        return {"routers": owned_routers}

    def get_all_ports(self):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/ports.json" % self.url_, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_owned_ports(self, tenant_id):
        ports = self.get_all_ports()
        owned_ports = []
        if ports is not None:
            for port in ports['ports']:
                if port['tenant_id'] == tenant_id:
                    owned_ports.append(port)
        return {"ports": owned_ports}

    def get_all_lbs(self):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/lb/pools.json" % self.url_, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_owned_lbs(self, tenant_id):
        lbs = self.get_all_lbs()
        owned_lbs = []
        if lbs is not None:
            for lb in lbs['pools']:
                if lb['tenant_id'] == tenant_id:
                    owned_lbs.append(lb)
        return {"pools": owned_lbs}

    def get_all_floatingips(self):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/floatingips.json" % self.url_, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_owned_floatingips(self, tenant_id):
        floatingips = self.get_all_floatingips()
        owned_floatingips = []
        if floatingips is not None:
            for floatingip in floatingips['floatingips']:
                if floatingip['tenant_id'] == tenant_id:
                    owned_floatingips.append(floatingip)
        return {"floatingips": owned_floatingips}

    def delete_network(self, network_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/networks/%s" % (self.url_,  network_id), headers=headers, verify=False)
        return r.status_code

    def delete_subnet(self, subnet_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/subnets/%s" % (self.url_,  subnet_id), headers=headers, verify=False)
        return r.status_code

    def delete_router(self, router_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/routers/%s" % (self.url_,  router_id), headers=headers, verify=False)
        return r.status_code

    def delete_pool(self, pool_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/lb/pools/%s" % (self.url_,  pool_id), headers=headers, verify=False)
        return r.status_code

    def delete_port(self, port_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/ports/%s" % (self.url_,  port_id), headers=headers, verify=False)
        return r.status_code

    def delete_router_interface(self, router_id, subnet_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        payload = json.dumps({'subnet_id': subnet_id})
        r = requests.put("%s/routers/%s/remove_router_interface" % (self.url_,  router_id), headers=headers, data=payload, verify=False)
        return r.status_code

    def get_all_agent_routers(self, agent_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/agents/%s/l3-routers.json" % (self.url_, agent_id), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_agents(self):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/agents.json" % self.url_, headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def remove_router_of_l3agent(self, l3agent_id, router_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/agents/%s/l3-routers/%s.json" % (self.url_,  l3agent_id, router_id), headers=headers, verify=False)
        return r.status_code

    def add_router_to_l3agent(self, l3agent_id, router_id):
        if self.token_ is None:
            return None
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        payload = {"router_id": router_id}
        r = requests.post("%s/agents/%s/l3-routers.json" % (self.url_, l3agent_id), headers=headers, data=json.dumps(payload), verify=False)
        if r.status_code == 201:
            return r.status_code
        raise Exception('HTTP Error:%s' % r.status_code)

    def set_network_quotas(self, tenant_id, network, subnetwork, router, floatingip, port, security_group,
                           security_group_rules, vip, pool):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json", "Accept": "application/json"}
        payload = {"quota": {"subnet": 1, "router": 1, "network": 1, "floatingip": 8, "port": 32, "security_group_rule": 0,
                             "security_group": 0, "vip": 0, "pool": 0}}
        payload["quota"]["network"] = network
        payload["quota"]["subnet"] = subnetwork
        payload["quota"]["router"] = router
        payload["quota"]["port"] = port
        payload["quota"]["floatingip"] = floatingip
        payload["quota"]["security_group"] = security_group
        payload["quota"]["security_group_rule"] = security_group_rules
        payload["quota"]["vip"] = vip
        payload["quota"]["pool"] = pool
        r = requests.put("%s/v2.0/quotas/%s.json" % (self.url_, tenant_id), headers=headers, data=json.dumps(payload),
                         verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data


