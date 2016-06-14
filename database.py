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

import mysql.connector
import logging


logger_ = logging.getLogger(__name__)

class Portal:
    """Database access to portal"""

    username_ = None
    password_ = None
    server_ = None
    schema_ = None
    port_ = None

    def __init__(self, server, username, password, schema='portal'):
        self.server_ = server
        self.username_ = username
        self.password_ = password
        self.schema_ = schema
    
    def getUserLanguage(self, email):
        cnx = mysql.connector.connect(user=self.username_, password=self.password_, database=self.schema_, host=self.server_)
        cursor = cnx.cursor()
        query = ("SELECT email, language FROM PORTAL_USER WHERE email like '%s'" % email)
        cursor.execute(query)
        for (email, language) in cursor:
            if language is None:
                language = "en"
            return language
        cursor.close()
        cnx.close()
        return "en"

    def updateEmailByUsernameAndCloud(self, username, email, cloud, language):
        cnx = mysql.connector.connect(user=self.username_, password=self.password_, database=self.schema_, host=self.server_)
        cursor = cnx.cursor()
        query = "UPDATE PORTAL_USER SET email='%s', language='%s' WHERE (username like '%s') and (cloud_id like '%s')" % (email, language, username, cloud)
        print query
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
        return
