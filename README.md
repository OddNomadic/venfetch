# Simple Venmo Client

I'm a forgetfull lad and sometimes need to do a bulk cross-referencing of
my bank statement with my venmo history in order to check whether my
roomates and I are fully and fairly caught up on debts such as utilities and rent.  

Venmo used to allow multple months of transaction history in its statements.
That does not appear to be the case currently, which is a shame.
The most basic goal of this project is to automate the concatenation
of multiple months of venmo transaction history into one easy to search
file.

# Installation
The primary intended method of installing dependencies for this project is to run:

```
pip install -r requirements.txt
```
or (if using Anaconda)
```
conda create --name <envname> --file requirements.txt
conda activate <envname>
```

# Usage
Create a file `credentials.txt` that has the format:
```
<Venmo email>
<Venmo password>
```
Where Venmo email and password are the credentials you typically use to log into 
Venmo
Example `credentials.txt`:
```
example@gmail.com
greatPass1234
```
These credentials will be used to log into Venmo when fetching statements.

To use the script:
```
python venfetch.py startDate [endDate] 
```
Where startDate and endDate are in "YYYY-mm-dd" format.  
startDate marks the beginning of the statement period you wish to fetch.  
endDate is optional and will default to today's date if not supplied. It marks
the end of the statement period you wish to fetch.

