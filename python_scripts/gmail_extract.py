from imap_tools import MailBox

# get all attachments from INBOX and save them to files
with MailBox('imap.gmail.com').login('tixieran', '#d!T8=dgfx6WS#@Ty7y0d', 'INBOX') as mailbox:
    for msg in mailbox.fetch():
        print(msg.subject)
        for att in msg.attachments:
            print('-', att.filename, att.content_type)
            with open('C:/1/{}'.format(att.filename), 'wb') as f:
                f.write(att.payload)