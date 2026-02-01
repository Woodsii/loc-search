# LoC-Search

A TUI Search engine for the Library of Congress' books. 

- [x] Script to download metadata from LoC website
- [x] Define tables based on the metadata we want
- [x] Parse the data from XML into CSVs that can be directly uploaded into postgres
- [x] Upload data to the db
- [ ] Define search table
- [ ] Integrate OpenSearch with search table
- [ ] Front end terminal application that can accessed via ssh

### Instructions
Pull repo into choosen dir:
```
git pull https://github.com/zachjesus/loc-search.git
```

Run the XML downloader:
```
./xml_downloader.sh
```
This pulls MARC Data from the 2016 Library of Congress Open Acecess collection.

Run the parser:
```
python3 parser.py
```
This convers the marc data into CSV's that can be uploaded directly into a Postgres databse with the format defined in tables.py

Install postgres:
```
apt install postgresql
```

Create db:
```
sudo su - postgres
psql
```

Into psql enter:
```
CREATE DATABASE locdb
```
If you do not use the name locdb then you will have to set the environment variable LOCDB_URL in the environment.

Create the base tables:
```
python3 tables.py
```

Run the uploader:
```
python3 uplaoder.py
```
Now the tables defined in tables.py will be filled with all of the datasets books!
