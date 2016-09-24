import urllib2
from bs4 import BeautifulSoup
import pandas as pd

def get_site_html(url):
    """
    Read an html page with the right settings.

    Parameters
    ----------
    url: string
        location of iesco bill
    """

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Ge\cko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    try:
        req = urllib2.Request(url, headers = hdr)
        source = urllib2.urlopen(req).read()
    except:
        source = []

    return source

def get_tree(url):
    """
    Parse an HTML page into a BeautifulSoup tree.

    Parameters
    ----------
    url: string
        location of iesco bill

    Returns
    -------
    tree: XML tree
    """

    source = get_site_html(url)
    try:
      tree = BeautifulSoup(source,'html.parser')
    except:
      tree = ''

    return tree

def parse(tree, id):
    """
    Parse XML tree to obtain billing and customer information.

    Parameters
    ----------
    tree: XML tree
        contains web page in XML format

    id: string
        customer reference number

    Returns
    -------
    data: pandas DataFrame
        Contains billing information (months, units, bills and 
        payments), customer information (name and address) and 
        customer reference number.
    """

    # Web page could not be retrieved
    if tree == '':
        return

    # Reference number is invalid
    elif len(tree.findAll('tr', {'style': 'height: 17px'})) == 0:
        return

    # Everything good, scrap data
    data = dict()
    tags = ['month', 'units', 'bill', 'payment']

    data['month'] = []
    data['units'] = []
    data['bill'] = []
    data['payment'] = []

    # Units consumed and bill for past several months
    for row in tree.findAll('tr', {'style': 'height: 17px'}):
        children = row.findChildren()
        for i in range(len(children)):
            s = children[i].text
            # Lots of spaces and \r\n. Clean before saving
            s = s.replace(' ', '').replace('\r\n', '')
            data[tags[i]].append(str(s))

    # customer name and address
    tree = tree.findAll('td', {'class': 'border-bt content'})
 

    if len(tree) != 0:
        t = tree[0].text    
        info = t.replace(' ', '').replace('\r\n', ' ').replace('\n', '')
        data['info'] = info
        data['id'] = id

    print data
    return data

def main():

    results = []
    # Random number for now. 
    id = 10141261799999

    # Again a random limit
    while id < 10141261999999:
        url = 'http://210.56.23.106:888/iescobill/general/'+str(id)
        tree = get_tree(url)
        data = parse(tree, str(id))
        
        if data is not None:
            results.append(data)
        id += 1

    # Save data
    df = pd.DataFrame(results)
    with open('data.csv', 'a') as f:
        df.to_csv(f, header=False)

if __name__ == '__main__':
    main()
