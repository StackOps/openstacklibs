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
from urllib import urlencode
import phpserialize
import base64

logger_ = logging.getLogger(__name__)

class WHMCS:

    username_ = None
    password_ = None
    url_ = None
    
    def __init__(self, url, username, password):
        self.username_ = username
        self.password_ = password
        self.url_ = url
        
    def __send(self, command, parameters={}):
        postFields = {
            'username': self.username_,
            'password': self.password_,
            'action': command,
            'responsetype':'json'}
        postFields.update(parameters)
        r = requests.post("%s" % self.url_, data=postFields)
        if r.status_code == 200:
            data = r.json()
            return data
        print r._content
        raise Exception('HTTP Error:%s' % r.status_code)


    def getClients(self):
        command = 'getclients'
        return self.__send(command)

    def getPendingOrders(self):
        command = 'getorders'
        params = {'status': 'Pending'}
        return self.__send(command, parameters = params)

    def acceptOrder(self, orderId):
        command = 'acceptorder'
        params = {'orderid': orderId,
                  'autosetup':True,
                  'sendemail':False}
        return self.__send(command, parameters = params)

    def getClientProducts(self, userId, productId):
        command = 'getclientsproducts'
        params = {'userid': userId, 'serviceid': productId}
        return self.__send(command, parameters = params)

    def getUser(self, userId):
        command = 'getclientsdetails'
        params = {'clientid': userId}
        return self.__send(command, parameters = params)

    def updateClientProductConfigOptions(self, serviceid, status = 'Active', configoptions = None):
        command = 'updateclientproduct'
        params = {'serviceid': serviceid,
                  'status': status}
        if configoptions is not None:
            x = phpserialize.dumps(configoptions)
            b64x = base64.b64encode(x)
            params.update({'customfields':b64x})
        return self.__send(command, parameters = params)
