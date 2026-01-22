import os
import re
import csv
from itertools import zip_longest
from lxml import etree
from multiprocessing import Pool

def process_file(file_path):
    ns = {'marc': 'http://www.loc.gov/MARC21/slim'}
    record_tag = '{http://www.loc.gov/MARC21/slim}record'

    match = re.search(r'\.part(\d+)\.xml$', file_path)
    part_num = int(match.group(1)) if match else 0
    part_str = f"part{str(part_num).zfill(2)}"
    book_id_base = part_num * 10_000_000

    print(f'Processing {file_path} into csvs...')

    books_file = open(f'/var/tmp/csvs/BooksAll.2016.books.{part_str}.csv', 'w', newline='')
    identifiers_file = open(f'/var/tmp/csvs/BooksAll.2016.identifiers.{part_str}.csv', 'w', newline='')
    publications_file = open(f'/var/tmp/csvs/BooksAll.2016.publications.{part_str}.csv', 'w', newline='')
    series_file = open(f'/var/tmp/csvs/BooksAll.2016.series.{part_str}.csv', 'w', newline='')
    subjects_file = open(f'/var/tmp/csvs/BooksAll.2016.subjects.{part_str}.csv', 'w', newline='')

    books_writer = csv.writer(books_file)
    identifiers_writer = csv.writer(identifiers_file)
    publications_writer = csv.writer(publications_file)
    series_writer = csv.writer(series_file)
    subjects_writer = csv.writer(subjects_file)

    context = etree.iterparse(file_path, events=('end',), tag=record_tag)
    record_num = 0

    for _, elem in context:
        record_num += 1
        book_id = book_id_base + record_num

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
                'heading': field.findtext("marc:subfield[@code='a']", namespaces=ns),
                'subheading': field.findtext("marc:subfield[@code='b']", namespaces=ns),
                'forms': field.xpath("marc:subfield[@code='v']/text()", namespaces=ns),
                'generals': field.xpath("marc:subfield[@code='x']/text()", namespaces=ns),
                'chrons': field.xpath("marc:subfield[@code='y']/text()", namespaces=ns),
                'geographics': field.xpath("marc:subfield[@code='z']/text()", namespaces=ns)
            }
            all_subjects.append(subject_entry)

        author = f"{personal_name} {dates}" if personal_name and dates else personal_name
        books_writer.writerow([book_id, author, title, remainder])

        for num in sys_control_nums:
            identifiers_writer.writerow([book_id, num])

        for place, publisher, pub_date in zip_longest(places, publishers, pub_dates):
            publications_writer.writerow([book_id, place, publisher, pub_date])

        for name in series_440 + series_490:
            series_writer.writerow([book_id, name, None])

        pg_arr = lambda items: '{' + ','.join('"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"' for v in items) + '}'
        for subj in all_subjects:
            subjects_writer.writerow([
                book_id,
                subj['heading'],
                subj['subheading'],
                pg_arr(subj['forms']),
                pg_arr(subj['generals']),
                pg_arr(subj['chrons']),
                pg_arr(subj['geographics'])
            ])

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    books_file.close()
    identifiers_file.close()
    publications_file.close()
    series_file.close()
    subjects_file.close()

if __name__ == '__main__':
    base_path = '/var/tmp/loc_data/BooksAll.2016.part{:02d}.xml'
    files = [base_path.format(i) for i in range(1, 43)]

    os.makedirs('/var/tmp/csvs', exist_ok=True)

    with Pool(processes=8) as pool:
        pool.map(process_file, files)