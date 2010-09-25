Don't Break The Chain Exporter
==============================

Overview
--------

The dbtc_exporter package will install a dbtcexporter command line
tool on your system.  It uses [Beautiful Soup][beautiful_soup],
[Twill][twill], and your Don't Break The Chain credentials to log in to 
[dontbreakthechain.com][dbtc] and save your chains to a CSV file.  

It will optionally save your chains to a JSON file for easy hacking. 

Installation
------------

Creating a [virtualenv][virtualenv] is optional but recommended.

    $ git clone https://timfreund@github.com/timfreund/dbtc_exporter.git
    $ cd dbtc_exporter
    $ python setup.py install

Want to hack on it instead? Scratch out that last line and run this instead:

    $ python setup.py develop

Usage
-----

    $ dbtcexporter -u my_username -p my_password -c my_dbtc_chains.csv --json-debug-output=my_dbtc_chains.json

The last two options are just that, optional.  No provided CSV location will
print your chain data to sys.stdout.  No json-debug-output will simply skip
the debug output step.  

Problems
--------

The script only looks as far back as the current year.  That's kinda
lame, and we should fix that.  

[beautiful_soup]: http://www.crummy.com/software/BeautifulSoup/
[twill]: http://twill.idyll.org/
[dbtc]: http://dontbreakthechain.com/
[virtualenv]: http://pypi.python.org/pypi/virtualenv
