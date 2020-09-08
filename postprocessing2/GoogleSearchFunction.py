## Dependencies
import logging
from googlesearch import search
## Other .py files
import LoggerFunction


def getFromGoogleSearch(searchText, siteBaseURL, WorkingDir):
    ## Basic Log Configuration
    googleResults = []
    logger = LoggerFunction.setup_logger('GoogleIt', WorkingDir+'\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    if isinstance(siteBaseURL, str):
        site = siteBaseURL.split('://')[1].lower()
        if site.startswith('www.'):
            site = site.replace('www.', '', 1)

    searchTerm = 'site:%s %s' % (site, searchText) if site else searchText

    logger.info('Using Google Search "%s"' % searchTerm)
    for URL in search(searchTerm, tld='com', lang='en', tbs='0', safe='off', num=10, start=0, stop=10, pause=2.0, country='', extra_params=None, user_agent=None, verify_ssl=True):
        googleResults.append(URL)
    
    return googleResults