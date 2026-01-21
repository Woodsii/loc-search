from lxml import etree
from multiprocessing import Pool
import csv

def process_file(file_path):
    ns = {'marc': 'http://www.loc.gov/MARC21/slim'}
    record_tag = '{http://www.loc.gov/MARC21/slim}record'
    
    context = etree.iterparse(file_path, events=('end',), tag=record_tag)

    for _, elem in context:
        # 035 - System Control Number (R)
        sys_control_nums = elem.xpath("marc:datafield[@tag='035']/marc:subfield[@code='a']/text()", namespaces=ns)

        # 100 Main Entry - Personal Name (NR)
        personal_name = elem.findtext("marc:datafield[@tag='100']/marc:subfield[@code='a']", namespaces=ns)
        dates = elem.findtext("marc:datafield[@tag='100']/marc:subfield[@code='f']", namespaces=ns)

        # 245 - Title Statement (NR)
        title = elem.findtext("marc:datafield[@tag='245']/marc:subfield[@code='a']", namespaces=ns)
        remainder = elem.findtext("marc:datafield[@tag='245']/marc:subfield[@code='b']", namespaces=ns)

        # 260 - Publication/Imprint (R)
        places = elem.xpath("marc:datafield[@tag='260']/marc:subfield[@code='a']/text()", namespaces=ns)
        publishers = elem.xpath("marc:datafield[@tag='260']/marc:subfield[@code='b']/text()", namespaces=ns)
        pub_dates = elem.xpath("marc:datafield[@tag='260']/marc:subfield[@code='c']/text()", namespaces=ns)

        # 440 - Series Statement (Retired) (R)
        series_440 = elem.xpath("marc:datafield[@tag='440']/marc:subfield[@code='a']/text()", namespaces=ns)
        
        # 490 - Series Statement (R)
        series_490 = elem.xpath("marc:datafield[@tag='490']/marc:subfield[@code='a']/text()", namespaces=ns)

        # 650 - Subject Statement (R)  
        all_subjects = []
        for field in elem.findall("marc:datafield[@tag='650']", namespaces=ns):
            subject_entry = {
                'heading': field.findtext("marc:subfield[@code='a']", namespaces=ns),        # (NR)
                'subheading': field.findtext("marc:subfield[@code='b']", namespaces=ns),     # (NR)
                'forms': field.xpath("marc:subfield[@code='v']/text()", namespaces=ns),      # (R)
                'generals': field.xpath("marc:subfield[@code='x']/text()", namespaces=ns),   # (R)
                'chrons': field.xpath("marc:subfield[@code='y']/text()", namespaces=ns),     # (R)
                'geographics': field.xpath("marc:subfield[@code='z']/text()", namespaces=ns) # (R)
            }
            all_subjects.append(subject_entry)

        # CSV WRITING

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

if __name__ == '__main__':
    files = []
    base_path = '/home/bennett/tmp/loc_data/BooksAll.2016.part{}.xml'
    
    for i in range(1, 43):
        files.append(base_path.format(str(i).zfill(2)))

    with Pool() as pool:
        pool.map(process_file, files)