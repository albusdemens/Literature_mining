import urllib, urllib2, sys
import xml.etree.ElementTree as ET

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

query = '("University of Copenhagen")'# AND ("1990"[Date - Publication])'

esearch = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&mindate=1901&maxdate=2014&retmode=xml&retmax=10000000&term=%s' % (query)
handle = urllib.urlopen(esearch)
data = handle.read()

root = ET.fromstring(data)
ids = [x.text for x in root.findall("IdList/Id")]
print 'Got %d articles' % (len(ids))

for group in chunker(ids, 100):
    efetch = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?&db=pubmed&retmode=xml&id=%s" % (','.join(group))
    handle = urllib.urlopen(efetch)
    data = handle.read()

    root = ET.fromstring(data)
    for article in root.findall("PubmedArticle"):
        pmid = article.find("MedlineCitation/PMID").text
        year = article.find("MedlineCitation/Article/Journal/JournalIssue/PubDate/Year")
        if year is None: year = 'NA'
        else: year = year.text
        aulist = article.findall("MedlineCitation/Article/AuthorList/Author")
        # Affiliation is the affiliation for the first author only
        affiliation = article.find("MedlineCitation/Article/AuthorList/Author/Affiliation")
        # print affiliation.text
        print pmid, year, len(aulist)
