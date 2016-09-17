# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import pprint
import json

apiKey = '44b3987b74343c72e5d14a4cd3f71c7f'

def findCustomerByName(username):
	url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)
	name_split = username.split()
	first_name = name_split[0]
	last_name = name_split[1]

	response = requests.get( 
		url, 
		headers={'content-type':'application/json'},
	)
	if response.status_code == 200:
		for obj in response.json():
			if obj['first_name'] == first_name and obj['last_name'] == last_name:
				return obj['_id']
	else: # failure, 
		print("Failure: can't find customer")
		return -1 # if customer is not found 

def createCustomer(username):
	url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)
	name_split = username.split()
	first_name = name_split[0]
	last_name = name_split[1]

	payload = {
  		"first_name": first_name,
  		"last_name": last_name,
  		"address": {
    		"street_number": "ds",
    		"street_name": "ds",
    		"city": "Cambridge",
    		"state": "MA",
    		"zip": "02138"
  		}
	}	

	# Create a Savings Account
	response = requests.post( 
		url, 
		data=json.dumps(payload),
		headers={'content-type':'application/json'},
	)


	if response.status_code == 201: # if success
		print("Success: create customer account")
	else: # if failure
		print("Failure: create customer account")
		return -1
	

def createAccount(username):
	customerId = findCustomerByName(username)
	if customerId == -1:
		createCustomer(username)
		customerId = findCustomerByName(username)

	url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
	payload = {
  		"type": "Savings",
  		"nickname": "test",
  		"rewards": 0,
  		"balance": 0,	
	}

	# Create a Credit Card Account
	response = requests.post( 
		url, 
		data=json.dumps(payload),
		headers={'content-type':'application/json'},
	)

	if response.status_code == 201:
		print('account created')
	else:	 
		return -1 # if account creation failed 

def getAccount(username):
	customerId = findCustomerByName(username)
	if customerId == -1:
		createAccount(username)
		customerId = findCustomerByName(username)

	url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId, apiKey)
	response = requests.get( 
		url, 
		headers={'content-type':'application/json'},
	)

	if response.status_code == 200:
		print('got account')
		obj = response.json()
		return (obj[0]['_id'], obj[0]['rewards'])
	else: 
		return -1 # if can't get account 

def depositPoints(accountId, points):
	url = 'http://api.reimaginebanking.com/accounts/{}/deposits?key={}'.format(accountId, apiKey)
	payload = {
  		"medium": "rewards",
  		"transaction_date": "2016-09-17",
  		"amount": points,
  		"description": "Rewards Points" 
	}
	response = requests.post( 
		url, 
		data=json.dumps(payload),
		headers={'content-type':'application/json'},
	)

	if response.status_code == 201:
		print('account updated')

# CALL this endpoint
# provide username as string of "firstname lastname", points is float value indicating how much points
# user gets for doing an action
def rewardCustomer(username, points):
	(accountId, rewards)  = getAccount(username) 
	depositPoints(accountId, points)

rewardCustomer("John Ho", 50)

# findCustomerByName("Mandela Patrick")