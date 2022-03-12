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
date_low = 201801010000
date_high = 201901010000

# get all attachments from INBOX and save them to files
with MailBox('imap.gmail.com').login(address, password, '[Gmail]/Sent Mail') as mailbox:
    for msg in mailbox.fetch():
        message_time_str = msg.date_str
        start = message_time_str.find(':') - 2
        end = start + 5
        message_time_str = message_time_str[start:end]
        message_time_str = message_time_str.replace(':','')
        #print(message_time_str)
        message_date = str(msg.date.year) + str(msg.date.month).rjust(2,'0') + str(msg.date.day).rjust(2,'0') 
        message_date = message_date + message_time_str
        message_date_int = int(message_date)
        print(message_date_int)
        if message_date_int >= date_high:
            break
        # Create Path if does not exist
        if message_date_int >= date_low and message_date_int < date_high:
            email = msg.html
            if email == '':
                email = msg.text
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
            sender = format(msg.from_values.name)
            sender = sender.replace(' ','') 
            sender = sender.replace('.','') 
            #print(sender)
            short_path = '/home/tixiera/gmail/inbox_exports/attachments/' + sender
            #print(short_path)
            email_long_path = short_path + '/' + subject
            #print(email_long_path)

            #print(subject)
            if not os.path.exists(short_path):
                print ('path ' + short_path + ' does not exist. Creating.')
                os.makedirs(short_path)
            # Save body of email
            print('Saving email ' + subject + ' from ' + sender)
            with open(email_long_path, 'w') as f:
                f.write(email)

            for att in msg.attachments:
                attach_cleaned_up_name = format(att.filename.strip())
                if attach_cleaned_up_name != '':
                    attach_cleaned_up_name = attach_cleaned_up_name.replace(' ','_') 
                    filename, file_extension = os.path.splitext(attach_cleaned_up_name)
                    attach_cleaned_up_name = filename + '_' + message_date + file_extension
                    pics_ext_list = ['.jpg','.JPG','jpeg','.JPEG','.png','.PNG','.gif','GIF','tiff','TIFF']
                    word_ext_list = ['.doc','.DOC','.docx', '.DOCX']
                    #print(attach_cleaned_up_name)
                    #print(file_extension)
                    if file_extension.upper() == '.PDF' or file_extension in pics_ext_list or file_extension in word_ext_list:
                        if not os.path.exists(short_path + '/pdf'):
                            print ('path ' + short_path + '/pdf' + ' does not exist. Creating.')
                            os.makedirs(short_path + '/pdf')
                        if not os.path.exists(short_path + '/pics'):
                            print ('path ' + short_path + '/pics' + ' does not exist. Creating.')
                            os.makedirs(short_path + '/pics')
                        if not os.path.exists(short_path + '/word'):
                            print ('path ' + short_path + '/word' + ' does not exist. Creating.')
                            os.makedirs(short_path + '/word')
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
                        # Save WORD Documents
                        if file_extension in word_ext_list:  
                            attach_long_path = short_path  + '/word/' + attach_cleaned_up_name  
                            print('Saving Word file ' + attach_cleaned_up_name)                     
                            #print('Saving Word file ' + attach_long_path)
                            with open(attach_long_path, 'wb') as f:
                                f.write(att.payload)