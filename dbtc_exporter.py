#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from optparse import OptionParser
from twill import get_browser
from xml.etree.ElementTree import ElementTree
import csv
import datetime
import re
import sys

def create_arg_parser():
    parser = OptionParser(usage="usage: %%prog\n%s" % __doc__)
    parser.add_option("-u", "--user", dest="user",
                      help="DBTC user")
    parser.add_option("-p", "--password", dest="password",
                      help="DBTC Password")
    parser.add_option("-c", "--csv",
                      dest="csv", 
                      help="Output file")
    return parser

class DBTCExporter(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = get_browser()
        self.logged_in = False

    def login(self):
        self.browser.go("http://dontbreakthechain.com/accounts/login")
        f = self.browser.get_all_forms()[0]
        f.set_value(value=self.username, name="username")
        f.set_value(value=self.password, name="password")
        self.browser._browser.form = f 
        self.browser.submit("login")
        self.logged_in = True        
        # TODO confirm login here

    def retrieve_all_data(self):
        chains = self.retrieve_chains()
        for chain in chains:
            chain_data = self.retrieve_chain_data(chain['id'])
            chain['data'] = chain_data
        return chains

    def retrieve_chains(self):
        if not self.logged_in:
            self.login()
        
        chain_soup = BeautifulSoup(self.browser.get_html())
        chain_list = chain_soup.find(attrs={'id': 'chains'})
        chain_links = chain_list.findAll(attrs={'class': 'chain'})
    
        chains  = []
        for chain_link in chain_links:
            chain = {}
            chain['name'] = chain_link.renderContents().strip()
            chain['id'] = chain_link.attrMap['href'].split('/')[-1]

            chains.append(chain)
        return chains

    def retrieve_chain_data(self, chain_id):
        chain_data = {}

        self.browser.go("http://dontbreakthechain.com/year/%s" % chain_id)
        chain_soup = BeautifulSoup(self.browser.get_html())
        days = chain_soup.findAll(attrs={'class': 'day day-hover link'})
        for day in days:
            date = day.attrMap['id'].split('_')[-1]
            chain_data[date] = True

        return chain_data


if __name__ == "__main__":
    parser = create_arg_parser()
    (options, args) = parser.parse_args()

    if None in [options.user, options.password]:
        print "Username and password is required" 
        parser.print_help()
        sys.exit(-1)

    exporter = DBTCExporter(options.user, options.password)
    chains = exporter.retrieve_all_data()

    # import json
    # json_decoder = json.JSONDecoder()
    # json_data_file = open("dbtc_data.json", "r")
    # json_data = json_data_file.read()
    # json_data_file.close()
    # chains = json_decoder.decode(json_data)

    header = ["date"]
    end_date = datetime.datetime.now()
    start_date = None
    for chain in chains:
        header.append(chain['name'])
        chain_start_date = min(chain['data'].keys())
        if start_date is None or chain_start_date < start_date:
            start_date = chain_start_date

    if options.csv is None:
        output_file = sys.stdout
    else:
        output_file = open(options.csv, "w")

    csv_writer = csv.writer(output_file)
    csv_writer.writerow(header)
    day = datetime.timedelta(1)
    date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    
    while(date < end_date):
        date_str = date.strftime("%Y-%m-%d")
        row = [date_str]
        for chain in chains:
            if chain['data'].has_key(date_str):
                row.append('X')
            else:
                row.append('')
        csv_writer.writerow(row)
        date = date + day

    output_file.close()
