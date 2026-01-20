from lxml import etree
from multiprocessing import Pool
import csv

def process_file(file_path):
    ns = {'marc': 'http://www.loc.gov/MARC21/slim'}
    record_tag = '{http://www.loc.gov/MARC21/slim}record'

    path_split = file_path.split('.') 
    path_split[-1] = 'csv' # replace .xml
    csv_path = '.'.join(path_split)
    

    context = etree.iterparse(file_path, events=('end',), tag=record_tag)

    for _, elem in context:
        personal_name = dates = sys_control_num = title = remainder = None
        place = name = date = series_name = volume = note = None
        topic_a = topic_b = form_v = gen_x = chron_y = geo_z = None
        
        # 035 - System Control Number (R)
        for field in elem.findall("marc:datafield[@tag='035']", namespaces=ns):
            sys_control_num = field.findtext("marc:subfield[@code='a']", namespaces=ns) # System control number

        # 100 Main Entry-Personal Name (NR)
        personal_name = elem.findtext("marc:datafield[@tag='100']/marc:subfield[@code='a']",
                                      namespaces=ns)
        dates = elem.findtext("marc:datafield[@tag='100']/marc:subfield[@code='d']",
                              namespaces=ns)

        # 245 - Title Statement (NR)
        title = elem.findtext("marc:datafield[@tag='245']/marc:subfield[@code='a']",
                              namespaces=ns)
        remainder = elem.findtext("marc:datafield[@tag='245']/marc:subfield[@code='b']",
                                  namespaces=ns)

        # 260 - Publication, Distribution, etc. (Imprint) (R)
        for field in elem.findall("marc:datafield[@tag='260']", namespaces=ns):
            place = field.findtext("marc:subfield[@code='a']", namespaces=ns) # Place of publication
            name = field.findtext("marc:subfield[@code='b']", namespaces=ns)  # Name of publisher
            date = field.findtext("marc:subfield[@code='c']", namespaces=ns)  # Date of publication

        # 440 - Series Statement/Added Entry-Title (R) *Retired, but still used in some places.
        for field in elem.findall("marc:datafield[@tag='440']", namespaces=ns):
            series_name = field.findtext("marc:subfield[@code='a']", namespaces=ns) # Title
            volume = field.findtext("marc:subfield[@code='v']", namespaces=ns)      # Volume/sequential designation

        # 490 - Series Statement (R)
        for field in elem.findall("marc:datafield[@tag='490']", namespaces=ns):
            series_name = field.findtext("marc:subfield[@code='a']", namespaces=ns)
            volume = field.findtext("marc:subfield[@code='v']", namespaces=ns)

        # 500 - General Note (R)
        for field in elem.findall("marc:datafield[@tag='500']", namespaces=ns):
            note = field.findtext("marc:subfield[@code='a']", namespaces=ns) # General note

        # 650 - Subject Added Entry-Topical Term (R)
        for field in elem.findall("marc:datafield[@tag='650']", namespaces=ns):
            subject_heading = field.findtext("marc:subfield[@code='a']", namespaces=ns) # Topical term or geographic name entry element
            subject_subheading = field.findtext("marc:subfield[@code='b']", namespaces=ns) # Topical term following geographic name entry element
            subject_form = field.findtext("marc:subfield[@code='v']", namespaces=ns)  # Form subdivision
            subject_general = field.findtext("marc:subfield[@code='x']", namespaces=ns)   # General subdivision
            subject_chron = field.findtext("marc:subfield[@code='y']", namespaces=ns) # Chronological subdivision
            subject_geographic = field.findtext("marc:subfield[@code='z']", namespaces=ns)   # Geographic subdivision
        
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