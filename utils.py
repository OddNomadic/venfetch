# This module will hold any functions that began impacting the
# readability of main a bit too much for my liking.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import twill.commands as tw
from twill.browser import TwillBrowser as TB
import twill
import io
from pandas import read_csv

# read the given file as a credentials file
# returns a tuple of email, password
# composing the user's Venmo Credentials
def readCreds(filePath):
    try:
        lines = open('credentials.txt').readlines()
        email, password = [line.strip() for line in lines]
    except Exception as e:
        print(f"problem loading credentials.txt: {e}")
    return email, password

def numMonths(startDate, endDate):
    return (endDate.year - startDate.year) * 12 + (endDate.month - startDate.month)
    
def formatRequest(startDate, endDate):
    startDate = startDate.strftime("%m-%d-%Y")
    endDate   = endDate.strftime("%m-%d-%Y")

    return f"statement?startDate={startDate}&endDate={endDate}"

def fetchUpToThreeMonths(startDate, endDate, accountID):
    if (endDate - startDate).days <= 90:
        url = "https://venmo.com/transaction-history/"          \
            + formatRequest(startDate, endDate)                 \
            + f"&profileId={accountID}&accountType=personal"
        tw.go(url)
        try:
            df = read_csv(io.StringIO(tw.show()), encoding='utf8', header=2)
            row, col = df.shape

            return df.drop([row-1])
        except Exception as e:
            print(f"problem reading response: {e}")
            return None
    else:
        raise Exception("Cannot fetch date range greater than 90 days")

def fetchRange(startDate, endDate, accountID):
    if startDate >= endDate:
        raise Exception(f"startDate {startDate} must be less than endDate {endDate}")
    if endDate > datetime.today():
        raise Exception(f"endDate {endDate} cannot be greater than today's date")

    firstDF = True
    statementDF = None

    # break this range up into 3 month chunks at most
    currentDate = startDate
    while currentDate <= endDate:
        if currentDate + relativedelta(days=90) > endDate:
            # clamp this fetch to endDate
            df = fetchUpToThreeMonths(currentDate, endDate, accountID)
        else:
            df = fetchUpToThreeMonths(currentDate, currentDate + relativedelta(days=90), accountID)

        if type(df) != type(None):
            if firstDF:
                statementDF = df
                firstDF = False
            else:
                statementDF = statementDF.append(df)
        
        currentDate = currentDate + relativedelta(days=90)
    
    return statementDF


