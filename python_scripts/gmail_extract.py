from imap_tools import MailBox

# get all attachments from INBOX and save them to files
with MailBox('imap.gmail.com').login('tixieran@gmail.com', "Fq0eNK7@BCD&I", 'INBOX') as mailbox:
    for msg in mailbox.fetch():
        #print(msg.subject)
        for att in msg.attachments:
            #print('-', att.filename, att.content_type)
            attach_name = '/home/tixiera/projects/gmail_extracts/attachments/' + format(att.filename.strip())
            print(attach_name)
            if attach_name != '/home/tixiera/projects/gmail_extracts/attachments/':
                #with open('/home/tixiera/projects/gmail_extracts/attachments/{}'.format(att.filename), 'wb') as f:
                with open(attach_name, 'wb') as f:
                    f.write(att.payload)