
import twill.commands as tw
import twill
import requests
import IPython
from pandas import read_csv
import utils
import argparse
"""
This script will take a start/end date as an input, log into Venmo with 
user-supplied credentials, and fetch statements in up to 3 month chunks 
(max Venmo allows) before concatenating them into one .csv
"""

if __name__ == '__main__':

    # configure arguments
    parser = argparse.ArgumentParser(description="A simple Venmo statement fetcher")
    parser.add_argument("startDate",    
                        nargs=1,    
                        type=lambda s: utils.datetime.strptime(s, '%Y-%m-%d'),
                        help="The date in YYYY-mm-dd format marking the \
                            beginning of the statement period")
    parser.add_argument("endDate",
                        type=lambda s: utils.datetime.strptime(s, '%Y-%m-%d'),
                        nargs='?',
                        default=utils.datetime.today(),
                        help="The date in YYYY-mm-dd format marking the \
                            end of the statement period. Defaults to today's date")
    args = parser.parse_args()
    startDate = args.startDate[0] 
    endDate   = args.endDate 


    # To make this easy for me to use as a personal tool,
    # but not have my email and password hardcoded, they
    # will be specified in a file called "credentials.txt"
    # The format of the file is:
    # ------------
    # <email>
    # <password>
    # ------------
    # where email is something like "example.com"
    # and password is the phrase you'd use to log into Venmo.
    email, password = utils.readCreds('credentials.txt')

    # read in email and password from credentials.txt
    # (what you normally use to log into venmo)

    tw.go('https://venmo.com/account/sign-in/')

    # there's an initial form on this page
    tw.fv('1', 'phoneEmailUsername', f'{email}')
    tw.fv('1', 'password', f'{password}')

    # push the first submit button on the page
    tw.submit('0')

    # a second, intermediate form...
    # Just needs the same information as the last one
    tw.fv('2', 'username', f'{email}')
    tw.fv('2',  'password', f'{password}')

    tw.submit('0')

    # Fetching transaction history involves a 'profileId' parameter.
    # it can be found on this page as 'external_id'
    tw.go('https://venmo.com/account/statement?end=03-26-2021&start=03-01-2021')
    page = tw.show()
    index = page.find('external_id')
    accountID = page[index:index+50].split(',')[0].split(':')[1].strip('"')

    df = utils.fetchRange(startDate, endDate, accountID)

    df.to_csv("statement.csv")
