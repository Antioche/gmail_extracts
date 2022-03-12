from imap_tools import MailBox
import os
import sys
import emoji

# Catch arguments one by one
address =  str(sys.argv[1])
password = str(sys.argv[2])

with MailBox('imap.gmail.com').login(address, password) as mailbox:
    # LIST
    for folder_info in mailbox.folder.list():
        print(folder_info) 


with MailBox('imap.gmail.com').login(address, password, '[Gmail]/Sent Mail') as mailbox:
    for folder_info in mailbox.folder.list():
        print(folder_info)
