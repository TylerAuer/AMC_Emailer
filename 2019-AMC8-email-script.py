#!/usr/bin/env python

"""
This program takes a CSV file and uses it to send AMC results to students in the Middle School.

See sample-data.csv for an example of the expected format of the csv
"""

import smtplib
import csv
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# File containing students data (including emails)
csvData = 'sample-data.csv'

# Opens csv file and adds row of CSV data as list within data
data = []
with open(csvData, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        data.append(row)


def amcAnswers(studentData):
    """
    Generates a string with:
    the question #, the student's answer, and the correct answer
    """
    # A list of the correct answers (updated for 2019 test)
    correctAnswers = ('D', 'E', 'E', 'D', 'B', 'C', 'A', 'E', 'B',
                      'B', 'D', 'A', 'A', 'C', 'B', 'D', 'B', 'C',
                      'C', 'D', 'E', 'E', 'B', 'B', 'C')
    finalString = ('Below you can see how you answered each question. '
                   'The correct answer is in parentheses. '
                   'A period represents a question you left blank.\n\n')

    # The first column in csv with a question
    questionStartIndex = 7

    questionNumber = 1
    for answer in studentData[questionStartIndex:]:
        finalString += "%s) %s (%s)\n" % (questionNumber,
                                          answer, correctAnswers[questionNumber - 1])
        questionNumber += 1

    finalString += "\n"
    return finalString


def amcBody(studentData):
    """
    Creates the body of an email with each student's AMC results and answers
    """
    # References for the data CSV (columns)
    nicknameIndex = 3
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
                   "with this link: https://artofproblemsolving.com/wiki/index.php/2019_AMC_8_Problems. \n\n")

    bodyString += "Please email Mr. Auer (TAuer@st-andrews.org) if you have any questions.\n"

    return bodyString


def sendEmails():

    # Sets up the connection to the mail server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    fromaddr = "AMC.Robot.Boop.Beep@st-andrews.org"
    password = raw_input("Enter password : ")
    # Need to enable unsafe applications or username, password combo will be rejected
    # Recommended that you use a throwaway email address (not your personal or work email address)
    # that way you aren't exposing your personal data
    server.login(fromaddr, password)

    # Generates and sends an email for each student
    for row in data[1:]:
        print row
        toaddr = row[2]
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'AMC Results'
        msg.attach(MIMEText(amcBody(row), 'plain'))
        server.sendmail(fromaddr, toaddr, msg.as_string())

    # Closes session on server
    server.quit()


sendEmails()
