from urllib import FancyURLopener
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re

# Make a new opener w/ a browser header so Google allows it
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    myopener = MyOpener()
    scholar_url = 'http://scholar.google.com/scholar?q=(query)&btnG=&hl=en&as_sdt=0%2C10'

# Define the search function for the google chart string
def findBetween(s, first, last):
    start = s.index(first) + len(first)
    end = s.index(last)
    return( s[start:end])

# Define the search for text within a string till the end othe string
def getX(s):
    start = s.index('chxl=0:') + len('chxl=0:')
    return( s[start:] )

# Define the function to actually get the chart data
def scholarCiteGet(link):
    # Navigate to and parse the user profile
    citLink2 = link.get('href')
    s2 = 'http://scholar.google.com' + citLink2
    socket = myopener.open(s2)
    wsource2 = socket.read()
    socket.close()
    soup2 = BeautifulSoup(wsource2)

    # Find the chart image and encode the string URL
    chartImg = soup2.find_all('img')[2]
    chartSrc = chartImg['src'].encode('utf=8')

    # Get the chart y-data from the URL
    chartD = findBetween(chartSrc, 'chd=t:', '&chxl')
    chartD = chartD.split(',')
    chartD = [float(i) for i in chartD]
    chartD = np.array(chartD)

    # Get the chart y-conversion
    ymax = findBetween(chartSrc, '&chxr=', '&chd')
    ymax = ymax.split(',')
    ymax = [float(i) for i in ymax]
    ymax = np.array( ymax[-1] )
    chartY = ymax/100 * chartD

    # Get the chart x-data
    chartX = getX(chartSrc)
    chartX = chartX.split('|')
    chartX = int(chartX[1])
    chartX = np.arange(chartX, 2014)
    chartTime = chartX - chartX[0]

    # put the data together and return a dataframe
    name = soup2.title.string.encode('utf-8')
    name = name[:name.index(' - Google')]
    d = {'name':name, 'year':chartX, 'lag':chartTime, 'cites':chartY}

    citeData = pd.DataFrame(d)

    return(citeData)

def scholarNameGet(name):

    # Navigate and parse the google scholar page with the search for the name specified
    name2 = name.replace(' ', '%20')
    s1 = ( scholar_url.replace('(query)', name2) )
    socket = myopener.open(s1)
    wsource1 = socket.read()
    socket.close()
    soup1 = BeautifulSoup(wsource1)

    # Get the link to the user profile
    citText = soup1.find_all(href=re.compile('/citations?') )

    if 'mauthors' in str(citText):
        citLink = citText[2]
        temp = scholarCiteGet(citLink)
        return(temp)
    else:
        citLink = citText[1]

    # If the link is to a user profile... get the data
    if 'User profiles' in str(citLink):
        temp = scholarCiteGet(citLink)
        return(temp)

    # If not, return 'no data'
    else:
        d = {'name':name, 'year':'No Data', 'lag':'No Data', 'cites':'No Data'}
        temp = pd.DataFrame(d, index=[0])
        return(temp)

# Run getCites once to populate the dataframe
finalDat = pd.DataFrame()

# Insert list of names here
sciNames = []

for name in sciNames:
    a = scholarNameGet(name)
    finalDat = pd.concat([finalDat, a])

plotDat = finalDat.pivot(index = 'lag', columns = 'name', values = 'cites')
plotDat = plotDat.replace('No Data', np.nan)
plotDat.plot()
