import email
import imaplib
import re
from bs4 import BeautifulSoup

def scrape(datastream):
    #test username: alexakomertest@gmail.com
    #test password: Test264737#
    # qwqrqeeqttquqy1
    username = datastream['email']
    password = datastream['password']
    maxparse = int(datastream['category'])

    domain = username.split('@')[1]
    domain = domain.split('.')[0]
    if(domain == "gmail"):
        site = "imap.gmail.com"
    else:
        site = "outlook.office365.com"
    try:
        mail = imaplib.IMAP4_SSL(site)
        mail.login(username,password)
    except email.errors.MessageError:
        print("invalid email or password")
    except:
        print("Some other error")
    
    mail.select("inbox")

    mail.create("Hazards")

    result, data = mail.uid('search', None, "ALL")

    inbox_item_list = data[0].split()

    hazardList = []

    counter = 0
    
    # for item in inbox_item_list:
    for item in range(len(inbox_item_list) - 1, 0, -1):
        
        if counter >= maxparse:
                break
            
        result2, emailData = mail.uid('fetch', inbox_item_list[item], '(RFC822)')

        raw_email = emailData[0][1].decode("utf-8")

        email_message = email.message_from_string(raw_email)

        recipient = email_message['To']
        sender = email_message['From']
        subject = email_message['Subject']
        date = email_message['date']
        
        
        
        
        for part in email_message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            filename = part.get_filename()
            content_type = part.get_content_type()
            if not filename:
                # if "plain" in content_type:
                if "html" in content_type:
                    # print(subject)
                    # print(date)
                    # print(part.get_payload())
                    try:
                        html_ = part.get_payload()
                        soup = BeautifulSoup(html_, "html.parser")
                        body = soup.get_text()
                    except:
                        print("Invalid file type")
                    # text = (body.split())
                    # body = ''
                    # for i in text:
                    #     body += i + ' '
                    # body = part.get_payload()
                    hazard = {}
                    email_data = {'recipient': recipient, 'sender': sender, 'subject': subject, 'date': date, 'body': body, 'hazard': hazard}
                    email_data['hazard'] = hazardous(email_data)
                    
                    if len(email_data['hazard']['tags']) != 0 or len(email_data['hazard']['credit']) != 0 or len(email_data['hazard']['social']) != 0: #Change back to NOT
                        hazardList.append(email_data)
        counter+=1
    return hazardList
                    


# Reads individual emails and determines if hazardous
def hazardous(data):
    
    hazards = {'tags': [], 'credit': [], 'social': []}
    subject = data['subject']
    lines = data['body']
    subject += lines
    lines = subject.lower()
    #Search for keywords
    valuable = ["social security","credit card","debit card", "credit info", "debit info", "password","username"]
    for eachSearch in valuable:
        if lines.find(eachSearch) != -1:
            hazards['tags'].append(eachSearch)
    # if hazards['tags'] == '':
    #     hazards['tags'] = 'None'
    #Search for credit/debit card numbers
    creditCards = []
    creditCardRegEx = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}')
    creditCards = creditCardRegEx.findall(lines)
    if creditCards:
        for eachCard in creditCards:
            newCredit = '****-****-****-'
            newCredit += eachCard[len(eachCard)-4:len(eachCard)]
            hazards['credit'].append(str(newCredit))
    # else:
    #     hazards['credit'].append('None')
    socialCards = []
    socialCardRegEx = re.compile(r'\d{3}-\d{2}-\d{4}')
    socialCards = socialCardRegEx.findall(lines)
    if socialCards:
        for eachCard in socialCards:
            newSocial = '***-**-'
            newSocial += eachCard[len(eachCard)-4:len(eachCard)]
            hazards['social'].append(str(newSocial))
    # else:
    #     hazards['social'].append('None')

    return hazards