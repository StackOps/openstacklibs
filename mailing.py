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

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from string import Template

import codecs

logger_ = logging.getLogger(__name__)

class Email:
    """Mailing the system"""

    username_ = None
    password_ = None
    server_ = None
    bcc_ = None
    from_ = None
    
    def __init__(self, username, password, frm, bcc, server = 'localhost:587'):
        self.server_ = server
        self.username_ = username
        self.password_ = password
        self.bcc_ = bcc
        self.from_  = frm
        
    def send(self, toaddrs, subj, msg, starttls = True, files=[]):
        mime = None
        if files is None:
            mime = MIMEText(msg, 'plain', 'utf-8')
        else:
            mime = MIMEMultipart('alternative')
            content = MIMEText(msg, 'plain', 'utf-8')
            mime.attach(content)
        mime['From'] = self.from_
        mime['To'] = ', '.join(toaddrs)
        mime['Bcc'] = self.bcc_
        mime['Subject'] = Header(subj, 'utf-8')
        for filename in files:
            f = file(filename)
            attachment = MIMEText(f.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            mime.attach(attachment)
        server = smtplib.SMTP(self.server_)
        server.ehlo()
        if starttls:
            server.starttls()
        server.login(self.username_, self.password_)
        server.sendmail(self.from_, toaddrs, mime.as_string())
        server.quit()
        logger_.info("Sent email to:'%s' subject:'%s'" % (toaddrs, subj))

class TemplateText:
    """Template in the system"""
    folder_ = None

    def __init__(self, folder="."):
        self.folder_ = folder
    
    def substitute(self, file, values):
        filein = codecs.open( '%s/%s' % (self.folder_,file), encoding='utf-8')
        src = Template( filein.read() )
        return src.substitute(values)
