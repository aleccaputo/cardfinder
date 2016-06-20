import praw
import time
import smtplib

r = praw.Reddit(user_agent = "Monitor a subreddit and get email notifications when there is a keyword hit")

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


looking = []
inputs = ''
while True:
	inputs = raw_input("Enter Keywords you are looking for. To add a new one, press enter. To finish type quit: ")
	if inputs == "quit":
		break
	else:
		looking.append(inputs)

cache= []

print(looking)

subr = raw_input('Enter the name of the subreddit you would like to monitor: ')
senderInput = raw_input('Enter the email you would like to send from: ')
recInput = raw_input('Enter the email you would like to receive notifications on: ')
passInput = raw_input('Enter the sending email address password: ')


def find_card():
	subreddit = r.get_subreddit(subr)
	for submission in subreddit.get_new(limit=10):
		isMatch = any(string in submission.title for string in looking)
		if submission.id not in cache and isMatch:

			print submission.title
			cache.append(submission.id)
			sender= senderInput
			receivers = recInput
			msg = MIMEMultipart()
			msg['From'] = sender
			msg['To'] = receivers
			msg['Subject'] ='New Sale!'
			
			body = submission.title
			link = submission.permalink
			ogLink = submission.url

			msg.attach(MIMEText(body.encode('utf-8'),'plain','utf-8'))
			msg.attach(MIMEText(link.encode('utf-8'),'plain','utf-8'))
			msg.attach(MIMEText(ogLink.encode('utf-8'),'plain','utf-8'))

			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(sender, passInput)
			text = msg.as_string()
			server.sendmail(sender, receivers, text)

			server.quit()


while True:
	find_card();
	time.sleep(10)
	
