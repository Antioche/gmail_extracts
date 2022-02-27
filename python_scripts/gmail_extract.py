from imap_tools import MailBox
import os
import sys
import emoji
# To remove emojis idiots in marketing put in email subjects
def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

# Catch arguments one by one
address =  str(sys.argv[1])
password = str(sys.argv[2])
#print (address)
#print (password)
date_low = 20171201
date_high = 20180101

# get all attachments from INBOX and save them to files
with MailBox('imap.gmail.com').login(address, password, 'INBOX') as mailbox:
    for msg in mailbox.fetch():
        message_date = str(msg.date.year) + str(msg.date.month).rjust(2,'0') + str(msg.date.day).rjust(2,'0')
        message_date_int = int(message_date)
        email = msg.html
        subject = format(msg.subject)
        subject = remove_emoji(subject)
        subject = subject.replace('/','-') 
        subject = subject.replace('.','_')
        subject = subject.replace(' ','_')
        subject = subject.replace(':','_') 
        subject = subject.replace('!','') 
        subject = subject.replace(',','_') 
        subject = subject.replace('"','') 
        subject = subject.replace("'",'') 
        subject = subject.replace(' ','_') + '_' + message_date + '.html'
        #print(subject)
        sender = format(msg.from_)
        sender = sender.replace(' ','') 
        #print(sender)
        short_path = '/home/tixiera/projects/gmail_extracts/exports/attachments/' + sender
        #print(short_path)
        email_long_path = short_path + '/' + subject
        #print(email_long_path)
        if message_date_int >= date_high:
            break
        
        for att in msg.attachments:
            if message_date_int >= date_low and message_date_int < date_high:
                attach_cleaned_up_name = format(att.filename.strip())
                if attach_cleaned_up_name != '':
                    attach_cleaned_up_name = attach_cleaned_up_name.replace(' ','_') 
                    filename, file_extension = os.path.splitext(attach_cleaned_up_name)
                    attach_cleaned_up_name = filename + '_' + message_date + file_extension
                    pics_ext_list = ['.jpg','.JPG','jpeg','.JPEG','.png','.PNG','.gif','GIF']
                    # print(attach_cleaned_up_name)
                    #print(file_extension)
                    if file_extension.upper() == '.PDF' or file_extension in pics_ext_list:
                        if not os.path.exists(short_path):
                            print ('path ' + short_path + ' does not exist. trying to make')
                            os.makedirs(short_path)
                        if not os.path.exists(short_path + '/pdf'):
                            print ('path ' + short_path + '/pdf' + ' does not exist. trying to make')
                            os.makedirs(short_path + '/pdf')
                        if not os.path.exists(short_path + '/pics'):
                            print ('path ' + short_path + '/pics' + ' does not exist. trying to make')
                            os.makedirs(short_path + '/pics')
                        # Save body of email
                        print('Saving email ' + subject + ' from ' + sender)
                        with open(email_long_path, 'w') as f:
                            f.write(email)
                        # Save PDFs
                        if file_extension.upper() == '.PDF': 
                            attach_long_path = short_path  + '/pdf/' + attach_cleaned_up_name                      
                            print('Saving PDF ' + attach_cleaned_up_name)
                            with open(attach_long_path, 'wb') as f:
                                f.write(att.payload)
                        # Save Pictures
                        if file_extension in pics_ext_list:  
                            attach_long_path = short_path  + '/pics/' + attach_cleaned_up_name  
                            print('Saving Picture ' + attach_cleaned_up_name)                     
                            #print('Saving Picture ' + attach_long_path)
                            with open(attach_long_path, 'wb') as f:
                                f.write(att.payload)