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
        
        # --- System Control Number (Tag 035) ---
        for field in elem.findall("marc:datafield[@tag='035']", namespaces=ns):
            sys_control_num = field.findtext("marc:subfield[@code='a']", namespaces=ns) # System control number

        # --- Main Entry-Personal Name (Tag 100) ---
        for field in elem.findall("marc:datafield[@tag='100']", namespaces=ns):
            personal_name = field.findtext("marc:subfield[@code='a']", namespaces=ns) # Personal name
            dates = field.findtext("marc:subfield[@code='d']", namespaces=ns)         # Dates associated with name

        # --- Title Statement (Tag 245) ---
        for field in elem.findall("marc:datafield[@tag='245']", namespaces=ns):
            title = field.findtext("marc:subfield[@code='a']", namespaces=ns)     # Title
            remainder = field.findtext("marc:subfield[@code='b']", namespaces=ns) # Remainder of title

        # --- Publication, Distribution, etc. (Imprint) (Tag 260) ---
        for field in elem.findall("marc:datafield[@tag='260']", namespaces=ns):
            place = field.findtext("marc:subfield[@code='a']", namespaces=ns) # Place of publication
            name = field.findtext("marc:subfield[@code='b']", namespaces=ns)  # Name of publisher
            date = field.findtext("marc:subfield[@code='c']", namespaces=ns)  # Date of publication

        # --- Series Statement/Added Entry-Title (Tag 440) ---
        for field in elem.findall("marc:datafield[@tag='440']", namespaces=ns):
            series_name = field.findtext("marc:subfield[@code='a']", namespaces=ns) # Title
            volume = field.findtext("marc:subfield[@code='v']", namespaces=ns)      # Volume/sequential designation

        # --- General Note (Tag 500) ---
        for field in elem.findall("marc:datafield[@tag='500']", namespaces=ns):
            note = field.findtext("marc:subfield[@code='a']", namespaces=ns) # General note

        # --- Subject Added Entry-Topical Term (Tag 650) ---
        for field in elem.findall("marc:datafield[@tag='650']", namespaces=ns):
            topic_a = field.findtext("marc:subfield[@code='a']", namespaces=ns) # Topical term or geographic name entry element
            topic_b = field.findtext("marc:subfield[@code='b']", namespaces=ns) # Topical term following geographic name entry element
            form_v = field.findtext("marc:subfield[@code='v']", namespaces=ns)  # Form subdivision
            gen_x = field.findtext("marc:subfield[@code='x']", namespaces=ns)   # General subdivision
            chron_y = field.findtext("marc:subfield[@code='y']", namespaces=ns) # Chronological subdivision
            geo_z = field.findtext("marc:subfield[@code='z']", namespaces=ns)   # Geographic subdivision
        
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