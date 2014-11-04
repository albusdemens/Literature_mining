from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(xml_data)

a_recs = []

for tag in soup.findAll("pubmedarticle"): # I'm working with multiple articles in one file
    for a_tag in tag.findAll("author"):
        a_rec = {}
        a_rec['pmid'] = int(tag.pmid.text)
        a_rec['lastname'] = a_tag.lastname.text
        a_rec['forename'] = a_tag.forename.text
        a_rec['suffix'] = a_tag.suffix.text
        a_rec['initials'] = a_tag.initials.text
        a_rec['affiliation'] = a_tag.affiliation.text
        a_recs.append(a_rec)
