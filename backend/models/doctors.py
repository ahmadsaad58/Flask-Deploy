import requests
import json
import urllib3

'''
File with anything that has to do with the doctors model
'''


def get_doctors_by_city(city):
	'''
	Function that gets up to 10 doctors by city

	Parameter
	--------
	city : str

	The city to search in 

	Returns
	-------

	The response
	'''

	requests.packages.urllib3.disable_warnings()
	requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
	try:
		requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
	except AttributeError:
		# no pyopenssl support used / needed / available
		pass
	
	# pull data with get 
	url = 'https://npiregistry.cms.hhs.gov/api/'
	querystring = {'version': '2.1', 'city': city.lower()}
	payload = ''
	response = requests.request('GET', url, data=payload, params=querystring, verify=False)
	return response


def parse_doc_data(response):
	'''
	Function that parses doctor data 

	Parameter
	---------
	response : response object

	Returns
	-------

	The count of doctors in the response and a dict of doc data (npi -> data)
	'''

	# load results
	count = json.loads(response.text)['result_count']
	results = json.loads(response.text)['results']

	# loop thru results and pull doc data
	# npi # -> data
	doc_data = {}
	for result in results:
		try:
			npi_number = result['number']
			doc_data[npi_number] = result
		except:
			print('NPI Number Missing')
			continue

	# returns count and dict of doctors
	return count, doc_data


def present(doc_data):
	'''
	Function to present data from passed in dictionary 

	Parameters
	----------
	doc_data : dict

	A dictionary with a variety of parameters that needs to be displayed
		- Name
			- Prefix
			- First Name
			- Middle Name
			- Last Name
			- Suffix 
			OR
			- Organization Name
		- Gender
		- Location
			- Address 1
			- Address 2
			- City
			- State
			- Postal Code
		- Phone
		- Taxonomies
			- all specialities
	
	Returns 
	-------

	A dictionary of doc_data (npi -> [parameters])

	'''

	ret = {}
	for npi, data in doc_data.items():
		basic = data['basic']
		
		# build name
		name = []
		if 'name_prefix' in basic:
			name.append( basic['name_prefix'].title() )
		if 'first_name' in basic:
			name.append( basic['first_name'].title() )
		if 'middle_name' in basic:
			name.append( basic['middle_name'].title() )
		if 'last_name' in basic:
			name.append( basic['last_name'].title() )
		if 'name_suffix' in basic:
			name.append( basic['name_suffix'].title() )
		
		# get organization 
		if 'organization_name' in basic:
			org = basic['organization_name'].split(',') 
			org.pop()
			name.append( ' '.join(org).title() )

		name = ' '.join(name)

		# build gender
		if 'gender' in basic:
			if basic['gender'] == 'M':
				gender = 'Male' 
			elif basic['gender'] == 'F':
				gender = 'Female'
		else:
			gender = '?'
		
		# TODO Add more data from basic

		# build location
		# type(addresses) = list
		addresses = data['addresses']
		location = []
		phone_number = ''
		fax_number = ''
		for address in addresses:
			# getting the physical address compared to mailing address
			if address['address_purpose'] == 'LOCATION':
				location.append( address['address_1'].title() )
				
				# if there is a unit/ste number
				if address['address_2'] != '':
					location.append( address['address_2'].title() )

				location.append( address['city'].title() )
				location.append( address['state'] )
				# add the dash between the first 6 nums and the last 4
				if len(address['postal_code']) > 6:
					location.append( address['postal_code'][:-4] + '-' + address['postal_code'][-4:] )
				else:
					location.append( address['postal_code'] )
				
				phone_number = address['telephone_number']
				try:
					fax_number = address['fax_number']
				except:
					fax_number = 'Not Found'
				# TODO Add more data from addresses
			else:
				continue
		
		location = ' '.join(location)

		
		# build taxonomies 
		# type(taxonomies) = list
		taxonomies = data['taxonomies']
		specialities = []
		for taxonomy in taxonomies:
			specialities.append(taxonomy['desc'])

		specialities = ', '.join(specialities)
		
		# print('name: {} \ngender: {} \nlocation: {} \ntaxonomies: {}\n'.format(name, gender, location, specialities))

		ret[npi] = {'full_name': name, 'gender': gender, 'location': location, 'phone': phone_number, 'fax': fax_number, 'specialities': specialities}

	return ret




def main(city):
	response = get_doctors_by_city(city)
	count, docs_in_austin = parse_doc_data(response)
	return present(docs_in_austin), count

if __name__ == "__main__":
	main('austin')
