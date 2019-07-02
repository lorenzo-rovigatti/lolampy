#!/usr/bin/env python3

from imapclient import IMAPClient, SEEN
import smtplib
import email.mime.text
import time

class GmailWrapper(object):
    def __init__(self, username, pwd):
        self.host = "imap.gmail.com"
        self.username = username
        self.pwd = pwd
        self.login()

    def login(self):
        self.incoming_server = IMAPClient(self.host, use_uid=True, ssl=True)
        self.incoming_server.login(self.username, self.pwd)
        self.incoming_server.select_folder("INBOX")
        
        self.outgoing_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.outgoing_server.ehlo()
        self.outgoing_server.login(self.username, self.pwd)

    def get_unread_ids(self):
        criteria = ["UNSEEN"]
        return self.incoming_server.search(criteria)

    def get_unread_ids_by_subject(self, subject):
        criteria = ["UNSEEN", "SUBJECT", subject]
        return self.incoming_server.search(criteria)

    def mark_as_read(self, ids):
        return self.incoming_server.set_flags(ids, [SEEN, ])

    def send_confirmation(self, address):
        sent_from = "%s@gmail.com" % self.username
        
        message = email.mime.text.MIMEText(u"Il motore ha girato alle %s" % time.strftime("%X del %x"))
        message['Subject'] = u"Lola si è cibata!"
        message['To'] = address
        message['From'] = sent_from
        
        self.outgoing_server.sendmail(sent_from, [address, ], message.as_string())
    