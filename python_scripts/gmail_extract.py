from imap_tools import MailBox
import os
import sys

# Catch arguments one by one
address =  str(sys.argv[1])
password = str(sys.argv[2])
#print (address)
#print (password)
date_low = 201712
date_high = 201801

# get all attachments from INBOX and save them to files
with MailBox('imap.gmail.com').login(address, password, 'INBOX') as mailbox:
    for msg in mailbox.fetch():
        message_date = str(msg.date.year) + str(msg.date.month).rjust(2,'0')
        message_date_int = int(message_date)
        email = msg.html
        subject = msg.subject
        #print(msg.subject)
        if message_date_int >= date_high:
            break
        
        for att in msg.attachments:
            if message_date_int >= date_low and message_date_int < date_high:
                attach_short_path = '/home/tixiera/projects/gmail_extracts/exports/attachments/' 
                attach_cleaned_up_name = format(att.filename.strip())
                attach_cleaned_up_name = attach_cleaned_up_name.replace(' ','_') 
                attach_long_path = attach_short_path + attach_cleaned_up_name
                print(attach_cleaned_up_name)
                #print(message_date)
                if not os.path.exists(attach_short_path):
                    print ('path ' + attach_short_path + 'does not exist. trying to make')
                    os.makedirs(attach_short_path)
                if not os.path.exists(attach_short_path + 'pdf'):
                    print ('path ' + attach_short_path + ' pdf' + 'does not exist. trying to make')
                    os.makedirs(attach_short_path + 'pdf')
                if not os.path.exists(attach_short_path + 'pics'):
                    print ('path ' + attach_short_path + ' pics' + 'does not exist. trying to make')
                    os.makedirs(attach_short_path + 'pics')
                # if there is something to save
                if attach_long_path != attach_short_path:
                    print('Saving ' + email)
                    with open(attach_short_path, 'wb') as f:
                        f.write(email.payload)
                    if attach_cleaned_up_name.endswith('.pdf'):                       
                        print('Saving ' + attach_cleaned_up_name)
                        with open(attach_long_path + 'pdf', 'wb') as f:
                            f.write(att.payload)