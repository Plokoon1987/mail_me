# Other python3 sources: #! /usr/local/bin/python3
# Other python3 sources: #! /usr/bin/python3
'''
    Script Design to work with Gmail mail server
'''

import sys
import os
import subprocess
import smtplib
from email.message import EmailMessage

def command_kwargs(args):
    for elem in args:
        key, val = elem.split('=')
        mail_vars[key] = val

##### Configuration variables (modifiables) #####
mail_vars = {
    'mail_server': 'smtp.gmail.com',
    'protocol_encription': 'ssl',
    'from_email': 'username@example.com',
    'from_email_pass': 'password',
    'to_email': ['user1@to_example.ie', 'user2@to_example.com'],
}

try:
    mail_vars['from_email'] = os.environ['MAIL_ME_FROM_EMAIL']
    mail_vars['from_email_pass'] = os.environ['MAIL_ME_FROM_EMAIL_PASS']
    mail_vars['to_email'] = [os.environ['MAIL_ME_TO_EMAIL_1']]
except:
    pass

##### Getting command kwargs #####
for elem in sys.argv[1:]:
    key, val = elem.split('=')
    mail_vars[key] = val

##### Other variables #####
mail_vars['mail_server_port'] = 465 if mail_vars['protocol_encription'] == 'ssl' else 587
my_ip = subprocess.run(['curl', 'ifconfig.me'], capture_output=True, text=True)

# SSl protocol #
if mail_vars['protocol_encription'] == 'ssl':
#    msg = EmailMessage()
#    msg['Subject'] = 'Tu nueva IP'
#    msg['From'] = mail_vars['from_email']
#    msg['To'] = mail_vars['to_email']
#    msg.set_content(my_ip.stdout)
#
#    with smtplib.SMTP_SSL(mail_vars['mail_server'], mail_vars['mail_server_port']) as smtp:
#        smtp.login(mail_vars['from_email'], mail_vars['from_email_pass'])
#
#        smtp.send_message(msg)


    with smtplib.SMTP_SSL(mail_vars['mail_server'], mail_vars['mail_server_port']) as smtp:
        smtp.login(mail_vars['from_email'], mail_vars['from_email_pass'])

        subject = 'Tu nueva IP'
        body = my_ip.stdout
        msg = 'subject: {}\n\n {}'.format(subject, body)

        smtp.sendmail(mail_vars['from_email'], mail_vars['to_email'], msg)

else:
    with smtplib.SMTP(mail_vars['mail_server'], mail_vars['mail_server_port']) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(mail_vars['from_email'], mail_vars['from_email_pass'])

        subject = 'Tu nueva IP'
        body = my_ip.stdout
        msg = 'subject: {}\n\n {}'.format(subject, body)

        smtp.sendmail(mail_vars['from_email'], mail_vars['to_email'], msg)
