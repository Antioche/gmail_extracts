from imap_tools import MailBox
import os

address = 'tixieran@gmail.com'
password = 'Fq0eNK7@BCD&I'
date_low = 201801
date_high = 201802

# get all attachments from INBOX and save them to files
with MailBox('imap.gmail.com').login(address, password, 'INBOX') as mailbox:
    for msg in mailbox.fetch():
        message_date = str(msg.date.year) + str(msg.date.month).rjust(2,'0')
        message_date_int = int(message_date)
        #print(msg.subject)
        if message_date_int >= date_high:
            break
        for att in msg.attachments:
            if message_date_int >= date_low and message_date_int < date_high:
                attach_write_path = '/home/tixiera/projects/gmail_extracts/attachments/' + message_date + '/'
                attach_write_name = attach_write_path + format(att.filename.strip())
                #print(message_date)
                if not os.path.exists(attach_write_path):
                    print ('path ' + attach_write_path + 'does not exist. trying to make')
                    os.makedirs(attach_write_path)
                if attach_write_name != attach_write_path:
                    print('Saving ' + attach_write_name)
                    with open(attach_write_name, 'wb') as f:
                        f.write(att.payload)