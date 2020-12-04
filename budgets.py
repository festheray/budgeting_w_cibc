import email, imaplib, os, re, csv

detach_dir = "."

#connect email via username & app token
user = os.environ['BUDGETS_EMAIL']
pwd = os.environ['BUDGETS_PASSWD']
url = 'imap.gmail.com'

m = imaplib.IMAP4_SSL(url)
m.login(user, pwd)

#choosing mailbox
m.select(mailbox='INBOX', readonly=False)
##### FOR TESTING: readonly=True

result, emailid = m.search(None, 'UnSeen', 'ALL') #grab emailid's of all unread New Purchases mails
emailid = emailid[0].split() # getting emailids in a list

#create lists for csv columns
csv_date = []
csv_amount = [] 
csv_vendor = [] 
csv_category = []

#import vendor category mappings as category_dict
from category_dict import category_dict

##########################
##### program starts #####
########################## 

for new in emailid: #each new unread mail
    resp, emailbody = m.fetch(new,'(RFC822)')
    # OTHER OPTIONS: RFC822 (UID BODY[TEXT])
    my_mail = email.message_from_string(emailbody[0][1].decode()) #decode emails into praseable format
    emailbody = str(emailbody)

    #date 
    date = re.findall('Date: (.*?) \-', emailbody)
    csv_date += date #add dates to csv

    #transaction amount
    amount = re.findall('\$\d{0,2}\,{0,1}\d{0,3}\.\d{0,2}', emailbody)

    transaction_type = email.header.decode_header(my_mail['Subject']) #type of transaction from emailSubject

    ##### func to categorize vendor by type #####
    def f_vendor_category():
    #categorize vendor, if found in category_dict
        for keys in category_dict: #search through keys in category_dict
            if keys in vendor: #if key matches this vendor
                global category
                category = (category_dict[keys]) #category is the value of the dict
                break
            else:
                category = ' '

    #new purchases
    if 'New purchase on your credit card' in str(transaction_type[0]):
        csv_amount += amount 
        vendor = re.findall('at (.*?)\.\<br', str(emailbody))
        csv_vendor += vendor
        vendor = str(vendor) #change vendor into string format to search in category_dict
        f_vendor_category() #categorize vendor using f_vendor_category
        csv_category += [category]

    #recurring purchases 
    elif 'New preauthorized payment with your credit card' in str(transaction_type[0]):
        csv_amount += amount 
        vendor = re.findall('to =\Sr\Sn(.*?) on your CIBC Dividend Visa', emailbody)
        csv_vendor += vendor
        vendor = str(vendor) #change vendor into string format to search in category_dict
        f_vendor_category() #categorize vendor using f_vendor_category
        csv_category += [category]

    #returns
    elif 'New purchase return on your credit card' in str(transaction_type[0]):
        csv_amount += ['-' + str(amount[0])]
        vendor = re.findall('\$\d{0,2}\,{0,1}\d{0,3}\.\d{0,2} from (.*?) o', emailbody)
        csv_vendor += vendor
        vendor = str(vendor) #change vendor into string format to search in category_dict
        f_vendor_category() #categorize vendor using f_vendor_category
        csv_category += [category]

    else: #didn't work?
        vendor += '??????????'

# write values to csv                 
with open('budgets.csv', 'a') as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerows(zip(csv_date, csv_amount, csv_vendor, csv_category))
