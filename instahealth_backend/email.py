import os
import yagmail

yag = yagmail.SMTP("instanthealthhackathon@gmail.com", os.environ["IH_PASSWORD"])

body = '''Hello,

A new question with your role has just been posted.

InstantHealth
'''

def send_email(to):
    yag.send(to=to, subject="New InstantHealth Question", contents=body)
