import csv
import urllib2

from billy.scrape import NoDataForPeriod
from billy.scrape.legislators import LegislatorScraper, Legislator


class CTLegislatorScraper(LegislatorScraper):
    state = 'ct'

    def scrape(self, chamber, term):
        if term != '2011-2012':
            raise NoDataForPeriod(term)

        office_code = {'upper': 'S', 'lower': 'H'}[chamber]

        leg_url = "ftp://ftp.cga.ct.gov/pub/data/LegislatorDatabase.csv"
        page = urllib2.urlopen(leg_url)
        page = csv.DictReader(page)

        for row in page:
            if office_code != row['office code']:
                continue

            name = row['first name']
            mid = row['middle initial'].strip()
            if mid:
                name += " %s" % mid
            name += " %s" % row['last name']
            suffix = row['suffix'].strip()
            if suffix:
                name += " %s" % suffix

            party = row['party']
            if party == 'Democrat':
                party = 'Democratic'

            leg = Legislator(term, chamber, row['dist'],
                             name, first_name=row['first name'],
                             last_name=row['last name'],
                             middle_name=row['middle initial'],
                             suffixes=row['suffix'],
                             party=party)
            leg.add_source(leg_url)
            self.save_legislator(leg)
