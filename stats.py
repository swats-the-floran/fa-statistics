#!/usr/bin/env python

'''
This is a statistics script for furaffinity art. It's needed when you have really many subscriptions and thousands
submissions and want to check if some artists can be removed from the subscriptions list.

Configuring:
1. change idir variable by showing your base art directory.
2. you can change names of database files but that's completely optional.

Usage: launch script and give it an address to the directory with downloaded furaffinity art before checking it.
Script will gather statistics about artists represented there and put it in text file called "_"
After watching art and removing art you don't like, launch script again and give it an address second time.
Script will gather new statistics, compare it with what was before and put new statistics in text file "__"
Overall statistics you can gather with time will be put in text file "stats" in the parent directory.
Main information you will get from this statistics is how much of some artist's images you liked and how much percent
of all downloaded art so you can decide if you really want to be subscribed to an artist which has less than 10% of
art you like but makes more than 10% of all art you watch.

To watch statistics you can open it with your favorite spreadsheet or even base text editor.
'''

import re
import sys
import os
import csv

# some base directory for shortening input. if you don't need it just make it an empty string
idir = '/home/user/Pictures/furaffinity/' + input()

# regex pattern for getting an artist's name from file name
ptrn = r'\b\d+[.](.+?)_'

poststat = {}

# filenames for before and after statistics "_" and "__" by default
initdbloc = '_'
postdbloc = '__'

# parent directory and filename for file with overall statistics
dbcom = os.path.join(idir, os.pardir, 'stats')


def csvWrite(file, adict, ttop):
    with open(file, 'w') as wt:
        writer = csv.writer(wt)
        writer.writerow(ttop)
        for i in adict:
            writer.writerow([i, i.getStats()])


def countFiles():
    # filling initial stats
    initstat = {}
    for file in files:
        artist = re.match(ptrn, file).group(1)
        quant_bef = (initstat[artist][0] + 1 if artist in initstat else 1)
        perct_bef = round(quant_bef * 100 / len(files), 2)
        initstat[artist] = [quant_bef, perct_bef]

    # showing most "productive" artists
    sort = sorted(initstat, key=lambda x: initstat[x][1], reverse=True)
    for i in sort[:10]:
        print(i, *initstat[i], sep='\t')

    return initstat


# removes artist's string from common stats
def remove(artist):
    with open(dbcom) as rd:
        lines = rd.readlines()
        lines = list(filter(lambda x: x.startswith(artist), lines))
    with open(dbcom, 'w') as wt:
        wt.writelines(lines)


# getting and filtering information from files
os.chdir(idir)
files = list(filter(os.path.isfile, os.listdir(idir)))
finish = initdbloc in files
files = list(filter(lambda x: re.match(ptrn, x) is not None, files))

# gathering initial statistics if files hadn't been checked yet
if not finish:
    initstat = countFiles()

    # writing initial stats and exit
    sort = sorted(initstat)
    with open('_', 'w') as initdbloc:
        writer = csv.writer(initdbloc)
        writer.writerow(['artist', 'quant before', '% before'])
        for i in sort:
            writer.writerow([i, *initstat[i]])
    os._exit(0)

# counting final stats and writing them in local csv dbf
with open(initdbloc) as dbloc, open(postdbloc, 'w') as dbloc_fin:
    currstat = countFiles()
    reader = csv.DictReader(dbloc)
    writer = csv.writer(dbloc_fin)
    writer.writerow(['artist', 'quant before', 'quant after', '% before', '% after', 'removed', '% rest'])
    for row in reader:
        artist = row['artist']
        quant_bef = int(row['quant before'])
        perct_bef = float(row['% before'])
        quant_aft = (currstat[artist][0] if artist in currstat else 0)
        perct_aft = (currstat[artist][1] if artist in currstat else 0)
        remvd = quant_bef - quant_aft
        perct_rst = round(quant_aft * 100 / quant_bef, 2)

        poststat[artist] = [quant_bef, quant_aft, perct_bef, perct_aft, remvd, perct_rst]
        writer.writerow([artist, *poststat[artist]])

# recounting and rewriting stats in common csv db file
with open(dbcom) as rd:
    reader = csv.DictReader(rd)
    dbcomstat = {}
    for row in reader:
        artist = row['artist']
        if artist in poststat:
            # counting
            quant_bef = int(row['quant before']) + poststat[artist][0]
            quant_aft = int(row['quant after']) + poststat[artist][1]
            summary = int(row['quant before']) * 100 / float(row['% before'])
            perct_bef = round(quant_bef * 100 / summary, 2)
            perct_aft = round(quant_aft * 100 / summary, 2)
            remvd = quant_bef - quant_aft
            perct_rst = round(quant_aft * 100 / quant_bef, 2)
        else:
            # just converting
            quant_bef = row['quant before']
            quant_aft = row['quant after']
            perct_bef = row['% before']
            perct_aft = row['% after']
            remvd = row['removed']
            perct_rst = row['% rest']

        dbcomstat[artist] = [quant_bef, quant_aft, perct_bef, perct_aft, remvd, perct_rst]
    # restore artists whose stats didn't change
    for artist in poststat:
        if artist not in dbcomstat:
            dbcomstat[artist] = poststat[artist]

    # and finally writing down
    with open(dbcom, 'w') as wt:
        writer = csv.writer(wt)
        writer.writerow(['artist', 'quant before', 'quant after', '% before', '% after', 'removed', '% rest'])
        sort = sorted(dbcomstat)
        for i in sort:
            writer.writerow([i, *dbcomstat[i]])
