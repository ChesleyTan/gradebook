from pymongo import MongoClient
from validation import *
import time
import datetime

# These helper functions are meant to be used in assembling the 
# messages package of variables used in the front end template

# Given a message string, creates a preview of it that is limited to 80 characters
def message_preview_conv(message):
	return message[:80]

# Given an epoch time t, return rounded string representation of the time 
# Suitable for use in the nearest time preview
def time_preview(t):
	date_time = datetime.datetime.fromtimestamp(t) # Creating a datetime object
	# From the epoch time for easy manipulation
	date_time_now = datetime.datetime.now()

	elapsed_time = date_time_now - date_time # A timedelta object
	seconds_elapsed = elapsed_time.seconds()
	# Time delta --> seconds
	# Now we want minutes
	minutes = seconds_elapsed / 60
	# Integer division --> 
	# Already rounded (estimate)
	return minutes

# Given student ID int, returns message target URL
def target_url(id):
	return "/message/" + str(id)

# This logic should be done in app.py in the interest of keeping 
# the templates clean / simple / free of Python
