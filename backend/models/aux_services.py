import requests
import json

'''
File with anything that has to do with the aux services model
'''


def get_aux_services_by_city(city):
	
	# pull data with get 
	url = 'https://data.medicare.gov/resource/ct36-nrcq.json'
	querystring = {'city': city.upper()}
	payload = ''
	response = requests.request('GET', url, data=payload, params=querystring)
	return response

def parse_aux_data(response):
    aux_data = {}
    i=0
    while(len(aux_data.keys()) < 3):
        company_name = response.json()[i]['dba_name']

        if(not company_name in aux_data):
            aux_data[company_name]=[response.json()[i]]
        else:
            aux_data[company_name].append(response.json()[i])
        i+=1
    
    return aux_data

def present(aux_data):
    ret = {}

    for dba_name in aux_data.keys():
        data = aux_data[dba_name]

        for i in range(len(data)):
            entry = data[i]
            if(i == 0):
                company_name=entry['company_name']

                # deals with store number
                if '#' in dba_name:
                    url = dba_name.replace('#', '%23')
                else:
                    url = dba_name
                #print(url)

                address = entry['address']
                city = entry['city']
                state = entry['state']
                zip_code = entry['zip']
                phone = entry['phone']
                product = [entry['prod_ctgry_name']]
                image = url + '.jpg'

                ret[dba_name] = {'url': url, 'name': company_name, 'address': address, 'city': city, 'state': state, 'zip code': zip_code, 'phone': phone, 'product': product, 'image': image}

                # todo: add competitive bid
            else:
                prod = entry['prod_ctgry_name']
                ret[dba_name]['product'].append(prod)
                #print(ret[dba_name]['product'])

    return ret

def main(city):
    response = get_aux_services_by_city(city)
    services_in_austin = parse_aux_data(response)
    return present(services_in_austin)

if __name__ == "__main__":
    main('austin')
