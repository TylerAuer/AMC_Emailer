#!/usr/bin/env python
# AMC Emailer
# Sends emails with AMC results to students

"""
This program takes a CSV file and uses it to send AMC results to the MS.

Known Bugs:
- Maximum logins gets exceeded and then you have to restart
    - Solution: Look in sent mail, delete up to last sent email in CSV file
"""

# TODO: Make it so sending each email is not a separate login
# TODO: Get a non-personal email

#!/usr/bin/env python

import smtplib
import csv
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

###
### MUST REMOVE HEADER ROW!
csvData = '/Users/teacher/desktop/AMC/8.csv' # Test file
# csvData = '/Users/teacher/desktop/AMC/results.csv' #Real file

# Makes a blank list to hold data
data = []

# Opens csv file and adds row of CSV data as list within list
with open(csvData, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        # adds row to data
        data.append(row)

#Subject of the emails
subject = 'Your Personalized AMC Results'

def amcAnswers(studentData):
    """
    Generates a string with:
    the question #,the student's answer, and the correct answer
    """
    # A list of the correct answers
    # Updated for 2019 test
    correctAnswers = ('D','E','E','D','B','C','A','E','B',
                      'B','D','A','A','C','B','D','B','C',
                      'C','D','E','E','B','B','C')
    finalString = ('Below you can see how you answered each question. '
                   'The correct answer is in parentheses. '
                   'A period represents a question you left blank.\n\n')
    
    # The first column with a question
    questionStartIndex = 7

    questionNumber = 1
    for answer in studentData[questionStartIndex:]:
        finalString += "%s) %s (%s)\n" % (questionNumber, answer, correctAnswers[questionNumber - 1])
        questionNumber += 1

    finalString += "\n"
    return finalString
                                          
def amcBody(studentData):
    """
    Creates the body of an email with each student's AMC results and answers
    """
    #References for the data CSV (columns)
    nicknameIndex = 3
    emailIndex = 2
    scoreIndex = 1
    
    bodyString = 'Dear %s,\n\n' % studentData[nicknameIndex]
    bodyString += ("This automated email contains your results for the AMC 8. \n\n"
    
                   "The AMC 8 is not graded like a normal test "
                   "because it is much harder. There aren't letter grades"
                   " and you don't get a percentage score. Instead, your score "
                   "is just how many questions you got right out of 25.\n\n"

                   "The test is taken by the strongest math students across "
                   "the world. But, even then, only 50% of the test takers "
                   "earn a score of 8 or higher. Only 25% of test takers "
                   "get 11 or more questions right. \n\n"

                   "Regardless of your score, you should be proud "
                   "that you took on the challenge of a really difficult "
                   "test. We encourage you to revisit the questions "
                   "using the link below.\n\n")

    bodyString += 'Your score was: %s.\n\n' % studentData[scoreIndex]

    bodyString += amcAnswers(studentData)

    bodyString += ("You can see the original questions and the answers "
                   "with this link: https://artofproblemsolving.com/wiki/index.php/2018_AMC_8_Problems. \n\n")

    bodyString += "Please email Mr. Auer if you have any questions.\n"
    
    return bodyString

def sendEmail(recipient, subject, body):
    """
    Sends an email from custom st-andrews.org account
    Expects strings for all .............
    """
    fromaddr = "AMC.Robot.Boop.Beep@st-andrews.org"
    toaddr = recipient
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
     
    body = body
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Will need to allow unsafe apps in Google interface
    server.login(fromaddr, raw_input("Enter password : ")) # Special login code here
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

for row in data:
    sendEmail(str(row[2]), "AMC 8 Results", amcBody(row))
