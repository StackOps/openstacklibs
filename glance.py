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


class Glance:
    """Glance in the system"""

    token_ = None
    url_ = None

    def __init__(self, token, url):
        self.token_ = token
        self.url_ = url

    def get_all_images(self):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.get("%s/images/detail" % (self.url_), headers=headers, verify=False)
        if r.status_code == 200:
            data = r.json()
            if 'error' in data:
                raise Exception(data['error']['message'])
        else:
            data = None
        return data

    def get_all_owned_images(self, tenant_id):
        images = self.get_all_images()
        private_images = []
        if images is not None:
            for image in images['images']:
                if image['owner'] == tenant_id:
                    private_images.append(image)
        return {"images": private_images}

    def delete_image(self, image_id):
        headers = {"X-Auth-Token": "%s" % self.token_, "Content-Type": "application/json"}
        r = requests.delete("%s/images/%s" % (self.url_, image_id), headers=headers, verify=False)
        return r.status_code



