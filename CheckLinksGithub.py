import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin

searched_links = []
broken_links = []

def getLinksFromHTML(html):
    def getLink(el):
        return el["href"]
    return list(map(getLink, BeautifulSoup(html, features="html.parser").select("a[href]")))

skipList = [
    'codeplayfield/actions',
#    'codeplayfield/blob',
#    'codeplayfield/branches',
#    'codeplayfield/commit',
    'codeplayfield/community',
#    'codeplayfield/compare',
#    'codeplayfield/dependencies'
    'codeplayfield/labels',
    'codeplayfield/issues',
    'codeplayfield/milestones',
#    'codeplayfield/network',
#    'codeplayfield/projects',
    'codeplayfield/pull',   # and pulls
    'codeplayfield/pulse',
    'codeplayfield/releases',
    'codeplayfield/search',
    'codeplayfield/security',
    'codeplayfield/stargazers',
    'codeplayfield/tags',
#    'codeplayfield/tree',
    'codeplayfield/watchers'
    ]

def find_broken_links(domainToSearch, url, parentUrl):
##    if ('github.com' in url) and ('animatedb/codeplayfield' not in url) or \
##        any(substring in url for substring in skipList):
##        pass
##    else:
        if (not (url in searched_links)) and (not url.startswith("mailto:")) and \
            (not ("javascript:" in url)) and (not url.endswith(".png")) and \
            (not url.endswith(".jpg")) and (not url.endswith(".jpeg")):
            try:
                requestObj = requests.get(url);
                searched_links.append(url)
                if(requestObj.status_code == 404):
                    broken_links.append("BROKEN: link " + url + " from " + parentUrl)
                    print(broken_links[-1])
                else:
                    print("NOT BROKEN: link " + url + " from " + parentUrl)
                    if urlparse(url).netloc == domainToSearch:
                        for link in getLinksFromHTML(requestObj.text):
                            find_broken_links(domainToSearch, urljoin(url, link), url)
            except Exception as e:
                print("ERROR: " + str(e));
                searched_links.append(domainToSearch)

def CheckLinks():
    # sys.argv[1]
#    url = 'https://github.com/animatedb/codeplayfield'
    url = 'https://animatedb.github.io/codeplayfield/Overview.html'
    find_broken_links(urlparse(url).netloc, url, "")

    print("\n--- DONE! ---\n")
    print("The following links were broken:")

    for link in broken_links:
        print ("\t" + link)

CheckLinks()

