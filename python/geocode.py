import requests
import pandas as pd
import re

# CHANGE BELOW WITH API KEY
API_KEY = 'put-api-key-here'
BASE = 'https://maps.googleapis.com/maps/api/geocode/json?address='

# TODO: One possible strategy to avoid a lot of calls to geocoding API
# is to only make one call per street. 

def add_geocodes(df):
    """
    Add geocodes to pandas dataframe.
    """

    ne_lat, ne_lng, sw_lat, sw_lng = [], [], [], []
    info = df['info']

    # Extract address 
    for i in info:
        address = i.split(' ')
        # Remove empty strings
        address = [a for a in address if a != '']

        try:
            address = address[2] + address[3]
        except:
            # Sometimes street and sector information is stacked together
            address = address[2]
        
        # If house address, format so that gecoding API can be applied
        if address[0] == 'h' or address[0] == 'H':
            split = re.split(r'([0-9]+)', address)
            address = 'Street ' + split[3] + ' '

            for s in split[4:-1]:
                address += s

            address += ' Islamabad'
        
        else:
            # TODO: When address belongs to a shop, industry etc.
            pass
        
        print address
        
        try:
            link = BASE + address + '&key=' + API_KEY
            r = requests.get(link)
            bounds = r.json()['results'][0]['geometry']['bounds']
            ne_lat.append(bounds['northeast']['lat'])
            ne_lng.append(bounds['northeast']['lng'])
            sw_lat.append(bounds['southwest']['lat'])
            sw_lng.append(bounds['southwest']['lng'])
            print 'Done'

        except:
            # Just in case API does not return expected result
            ne_lat.append('')
            ne_lng.append('')
            sw_lat.append('')
            sw_lng.append('')
            print 'Bad'     

    df['ne_lat'] = ne_lat
    df['ne_lng'] = ne_lng
    df['sw_lat'] = sw_lat
    df['sw_lng'] = sw_lng

    df.to_csv('data_geocoded.csv')
    
def main():
    df = pd.read_csv('data.csv')
    add_geocodes(df)

if __name__ == '__main__':
    main()


