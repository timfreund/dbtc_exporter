#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from optparse import OptionParser
from twill import get_browser
from xml.etree.ElementTree import ElementTree
import re

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
        browser.go("http://dontbreakthechain.com/accounts/login")
        f = browser.get_all_forms()[0]
        f.set_value(value=self.username, name="username")
        f.set_value(value=self.password, name="password")
        browser._browser.form = f 
        browser.submit("login")
        self.logged_in = True
        
        # TODO confirm login here

    def retrieve_chains(self):
        if not self.logged_in:
            self.login()
        
        chain_soup = BeautifulSoup(self.browser.get_html())
        chain_list = chain_soup.find(attrs={'id': 'chains'})
        chain_links = chain_list.findAll(attrs={'class': 'chain'})
    
        self.chains  = []
        for chain_link in chain_links:
            chain = {}
            chain['name'] = chain_link.renderContents().strip()
            chain['id'] = chain_link.attrMap['href'].split('/')[-1]

            self.chains.append(chain)

    def retrieve_chain_data(self, chain_name):
        target = None
        for chain in self.chains:
            if chain['name'] == chain_name:
                target = chain
        
        if target is None:
            raise Exception("No such chain")

        self.browser.go("blah/blah/%s" % target['id'])
        chain_soup = BeautifulSoup(self.browser.get_html())
        days = chain_soup.findAll(attrs={'class': 'day day-hover link'})
        for day in days:
            print day.attrMap['id'].split('_')[-1]


if __name__ == "__main__":
    html_file = open("40783.html")
    html = html_file.read()
    html_file.close()

    chains = []

    # chain_doc = ElementTree(file="40783.html")
    chain_soup = BeautifulSoup(html)
    chain_list = chain_soup.find(attrs={'id': 'chains'})
    chain_links = chain_list.findAll(attrs={'class': 'chain'})
    
    for chain_link in chain_links:
        chain = {}
        chain['name'] = chain_link.renderContents().strip()
        chain['id'] = chain_link.attrMap['href'].split('/')[-1]

        chains.append(chain)

    print chains

    days = chain_soup.findAll(attrs={'class': 'day day-hover link'})
    for day in days:
        print day.attrMap['id'].split('_')[-1]



    b = get_browser()
    b.go("http://dontbreakthechain.com/accounts/login")
    f = b.get_all_forms()[0]
    f.set_value(value="my_username", name="username")
    f.set_value(value="my_password", name="password")
    b._browser.form = f 
    b.submit("login")
    html = b.get_html()

