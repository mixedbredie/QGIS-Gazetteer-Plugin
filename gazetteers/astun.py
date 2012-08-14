'''
Created on Aug 14, 2012

@author: Nathan Woodrow
'''

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from gazetter import SearchResult
from json import loads

class AstunJson():
    #TODO Refactor this out into config.ini
    name = 'AstunTechnology'
    url = 'http://test.astuntechnology.com/iShareLatest.web/getdata.aspx'
    data = {
            'type': 'json',
            'RequestType':'LocationSearch',
            'gettotals':'true',
            'axuid': 1344265603167,
            'mapsource': 'Workshop/MyHouse',
            '_': 1344265603168}
    
    def getUrlAndData(self, query):
        self.data['location'] = query
        self.data['pagesize'] = 6
        self.data['startnum'] = 1
        return (self.url, self.data)
        
    def parseURLResults(self, data):
        json_result = loads(data)
        columns = json_result['columns']
        for item in json_result['data']:
             mapped = dict(zip(columns,item)) 
             result = SearchResult(self.name)
             result.description = mapped['Name']
             result.x = float(mapped['X'])
             result.y = float(mapped['Y'])
             result.zoom = float(mapped['Zoom'])
             yield result

if __name__ == "__main__":
    # Just some quick test logic. TODO Remove.
    from urllib2 import urlopen
    from urllib import urlencode
    astun = AstunJson()
    url, data = astun.getUrlAndData(10)
    params = urlencode(data)
    data = urlopen(url + "?" + params).read()
    results = astun.parseURLResults(data)
    for res in results:
        print res.description, res.x, res.y, res.zoom
    
    