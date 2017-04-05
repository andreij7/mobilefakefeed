import json
import re

import falcon
import os.path
import urllib

class FeedsResource(object):

    def __init__(self, market):
        self.market = market

    def getFileName(self, url):
        regex = re.compile('[^a-zA-Z0-9]')

        onlyLettersNumbers = regex.sub('', url);

        try:
            comIndex = onlyLettersNumbers.index("com")
        except:
            return 'nocom.txt'

        try:
            consumerIndex = onlyLettersNumbers.index("consumer")

            fileName =  onlyLettersNumbers[comIndex + 3: consumerIndex]  + '.json'
        except ValueError:
            fileName =  onlyLettersNumbers[comIndex + 3:]  + '.json'

        if ('apikey' in fileName):
            fileName = fileName[:fileName.index('apikey')] + '.json'

        return fileName.lower()

    def getPath(self, url):
        try:
            comIndex = url.index("com")
        except:
            return ''

        try:
            consumerIndex = url.index("consumer")

            return url[comIndex: consumerIndex]
        except:
            return url[comIndex + 3: ]

    def getSaveJson(self, url, api_key, fileName):
        if (not url.startswith("http://")): return False;


        if('MetaData.svc/leagues' not in url):
            url = url + "&api_key=" + api_key

        with open(self.market + '/filefeed.txt', 'a') as urlList:
            resource = fileName.replace('.json','')

            path = self.getPath(url)

            line = 'fileFeeds.add(new FileFeed("' + path + '", com.gannett.android.news.test.R.raw.' + resource  + '));'

            #urlList.write('//' + url + '\n')
            urlList.write(line + '\n')

        response = urllib.urlopen(url)

        data = json.loads(response.read())

        with open(self.market + '/' + fileName, 'w') as outfile:
            json.dump(data, outfile)

        return True;

    def on_get(self, req, resp):
        url = req.get_param('url', True)

        if('internal' in url): print url

        fileName = self.getFileName(url)

        if(fileName.endswith('nocom.txt')): return

        if not os.path.isfile(self.market + '/' + fileName):
            if('api_key' in url):
                api_key = url[url.index('api_key') + 8:]
            else:
                api_key = req.get_param('api_key', True)

            shouldContinue = self.getSaveJson(url, api_key, fileName)
            if( not shouldContinue):
                return

        with open(self.market + '/' + fileName) as data_file:
            data = json.load(data_file)

        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        resp.body = json.dumps(data)



