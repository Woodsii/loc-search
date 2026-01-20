from lxml import etree

record_tag = '{http://www.loc.gov/MARC21/slim}record'

for i in range(1, 43):
    part_num = str(i).zfill(2)
    path = '/home/tmp/loc_data/BooksAll.2016.part' + part_num + '.xml'

    context = etree.iterparse(path, events=('end'), tag=record_tag)

    for event, elem in context:
        # do record parse here

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]