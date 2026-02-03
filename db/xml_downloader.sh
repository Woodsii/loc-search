#!/bin/bash
# xml_downloader.sh

mkdir -p /var/tmp/loc_data
cd /var/tmp/loc_data

curl -L -O "https://www.loc.gov/cds/downloads/MDSConnect/BooksAll.2016.part[01-42].xml.gz"

gzip -d *.gz

echo "Done! Files in /var/tmp/loc_data/"