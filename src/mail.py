#!/usr/bin/env python3

from imapclient import IMAPClient, SEEN

class GmailWrapper(object):
    def __init__(self, username, pwd):
        self.host = "imap.gmail.com"
        self.username = username
        self.pwd = pwd
        self.login()

    def login(self):
        self.server = IMAPClient(self.host, use_uid=True, ssl=True)
        self.server.login(self.username, self.pwd)
        self.server.select_folder("INBOX")

    def get_unread_ids(self):
        criteria = ["UNSEEN"]
        return self.server.search(criteria)

    def get_unread_ids_by_subject(self, subject):
        criteria = ["UNSEEN", "SUBJECT", subject]
        return self.server.search(criteria)

    def mark_as_read(self, ids):
        return self.server.set_flags(ids, [SEEN, ])
