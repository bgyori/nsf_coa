__all__ = ['get_records_for_pmid', 'get_records_for_pmids',
           'get_table_for_pmids']

import sys
import tqdm
import pandas as pd
from indra.literature import pubmed_client


month_mapping = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}


def get_records_for_pmid(pmid):
    x = pubmed_client.get_full_xml(pmid)
    author_tags = x.findall('.//AuthorList/Author')
    pub_date_tag = x.find('.//PubDate')
    year = pub_date_tag.find('Year').text
    month_tag = pub_date_tag.find('Month')
    month = month_tag.text if month_tag is not None else 'Jan'
    day_tag = pub_date_tag.find('Day')
    day = day_tag.text if day_tag is not None else '1'
    formatted_date = f"{month_mapping[month]}/{int(day)}/{year}"

    records = []

    for author_tag in author_tags:
        collective_name = author_tag.find('CollectiveName')
        if collective_name is not None:
            continue
        last_name = author_tag.find('LastName').text
        first_name = author_tag.find('ForeName').text
        affil1 = author_tag.find('AffiliationInfo/Affiliation').text
        records.append(
            {
                '4': 'A:',
                'Name:': f"{last_name}, {first_name}",
                'Organizational Affiliation': affil1,
                'Optional  (email, Department)': '',
                'Last Active': formatted_date,
                'PMID': pmid
            }
        )
    return records


def get_records_for_pmids(pmids, merge=True):
    records = []
    for pmid in tqdm.tqdm(pmids):
        records.extend(get_records_for_pmid(pmid))

    # The logic here aims to
    # 1. Recognize duplicate names
    # 2. Find the most recent date the name appears
    # 3. Return the sorted and merged records
    if merge:
        records_dict = {}
        for record in records:
            name = record['Name:']
            last_active = record['Last Active']
            # We need to turn the date into a sortable format
            last_active = pd.to_datetime(last_active, format='%m/%d/%Y')
            if name not in records_dict:
                records_dict[name] = {'Last Active': last_active,
                                      'record': record}
            if last_active > records_dict[name]['Last Active']:
                records_dict[name]['Last Active'] = last_active
                records_dict[name]['record'] = record

        merged_records = []
        for name, record_dict in records_dict.items():
            record = record_dict['record']
            # We need to render the date as e.g., 12/30/2024
            record['Last Active'] = \
                record_dict['Last Active'].strftime('%m/%d/%Y')
            merged_records.append(record)

        records = merged_records

    records = sorted(records, key=lambda x: x['Name:'])

    return records


def get_table_for_pmids(pmids, merge=True):
    records = get_records_for_pmids(pmids, merge=merge)
    df = pd.DataFrame(records)
    return df


if __name__ == '__main__':
    pmids = sys.argv[1:]
    df = get_table_for_pmids(pmids)
    df.to_excel(f'coa.xlsx', index=False)

