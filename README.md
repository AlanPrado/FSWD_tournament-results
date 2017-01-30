#Project: Tournament Results

Build a database schema in postgresql
that describes a model for Swiss-system tournament.

## Quick start

- Download and install [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
- Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
- Clone the repo: `https://github.com/AlanPrado/tournament-results/`
- Run: `vagrant up` to setup vagrant
- Run: `vagrant ssh` to enter into VM
- Run: `python /vagrant/tournament/tournament_test.py` to test

Note that you should not change any .css files in order to change the style.
Change *.scss files and *.css files will be automatic generated with the modifications.

### What's included

Within the download you'll find tournament directory.
```
├ tournament.py      # perform queries
├ tournament.sql     # ddl script files
└ tournament_test.py # test tournament.py queries
```

## Copyright and license
Code and documentation copyright 2017-2017 Code released under the [MIT License](https://github.com/AlanPrado/tournament-results/master/LICENSE)

## Authors

#### Original Author and Development Lead

- Alan Thiago do Prado (aprado.cnsp@gmail.com)