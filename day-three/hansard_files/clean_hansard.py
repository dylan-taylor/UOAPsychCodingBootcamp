import re
import csv
import pandas as pd

class Section:
    def __init__(self, section_type, section_time, section_date, section_content, section_speaker = None, section_party = None):
        self.section_type = section_type
        self.section_time = section_time
        self.section_date = section_date
        self.section_content = section_content
        self.section_speaker = section_speaker
        self.section_party = section_party

    def __str__(self):
        return f"type: {self.section_type}\n time: {self.section_time}\n date: {self.section_date}\n speaker: {self.section_speaker}\n party: {self.section_party}\n  content: {self.section_content}"
    
    def __repr__(self):
        return f"type: {self.section_type}\n time: {self.section_time}\n date: {self.section_date}\n speaker: {self.section_speaker}\n party: {self.section_party}\n  content: {self.section_content}"
    
    def set_content(self, content):
        self.section_content = content

    def append_contect(self, content):
        self.section_content += content

    def determine_speaker(self):
        speaker_pattern = re.compile('<strong>(.*)</strong>:')
        strong_pattern = re.compile('<strong>|</strong>')
        party_pattern = re.compile('\(.*\).*')
        num_pattern = re.compile('\d*\. ')
        speaker_match = speaker_pattern.search(self.section_content)
        if speaker_match:
            speaker_no_strong = re.sub(strong_pattern, '', speaker_match[1])
            speaker_no_party = re.sub(party_pattern, '', speaker_no_strong)
            speaker_name = re.sub(num_pattern, '', speaker_no_party)
            self.section_speaker = remove_honorifics(speaker_name).strip().lower()
        else:
            self.section_speaker = "admin"

    def determine_party(self, party_list):
        if self.section_speaker in list(party_list["name"]):
            self.section_party = party_list.loc[party_list["name"]==self.section_speaker, "party"].values[-1]
        else:
            self.section_party = "admin"
    
    def clean_content(self):
        self.section_content = re.sub('.*</strong>: ', '', self.section_content)
        self.section_content = re.sub('<.*?>', '', self.section_content)

    def extract_details(self, party_list):
        self.determine_speaker()
        self.determine_party(party_list)
        self.clean_content()

def load_html(load_file):
    with open(load_file, "r") as f:
        return f.read()[1:-1]

def load_blacklist():
    with open("section_blacklist.txt", "r") as f:
        return f.read().split("\n")
    
def get_sections(scrapings):
    div_split = scrapings.split('<div class="section">')
    type_content_pattern = re.compile('<p class="(.*?)">(.*?)</p>')
    time_pattern = re.compile('<a name="time_(\d*) (\d*:\d*:\d*)"></a>')
    section_list = []

    for div in div_split:
        type_content_split = type_content_pattern.findall(div)
        for type_content_match in type_content_split:
            section_type = type_content_match[0]
            section_content = type_content_match[1]
            time_match = time_pattern.search(section_content)
            section_date = time_match[2] if time_match else "None"
            section_time = time_match[1] if time_match else "None"
            section_list.append(Section(section_type, section_date, section_time, section_content))
    
    return section_list
    
def stich_sections(sections):
    stiched_sections = []
    content_accumulator = []
    head_section = sections[0]
    for section in sections[1:]:
        if section.section_type == "a":
            head_section.append_contect(section.section_content)
        else:
            stiched_sections.append(head_section)
            head_section = section
    stiched_sections.append(head_section)

    return stiched_sections

def clean_sections(sections):
    clean_list = []
    section_type_blacklist = load_blacklist()
    for section in sections:
        if not section.section_type in section_type_blacklist:
            clean_list.append(section)
    return clean_list

def remove_honorifics(name):
    honorifics = ["Dr", "Hon", "Rt"]
    for honorific in honorifics:
        name = name.replace(honorific+" ", "")
    return name

def load_party_affiliation():
    member_parties = pd.read_csv("member_list_full.csv")
    name_list_raw = [remove_honorifics(name).lower() for name in member_parties["Name"]]
    party_list_raw = [str(party).lower() for party in member_parties["Party"]]

    party_list = []
    for party in party_list_raw:
        if party == "nan":
            party_list.append("independant")
        else:
            party_list.append(party)
        name_list = []

    for name in name_list_raw:
        name_split = name.split(",")
        name_joined = name_split[1].strip() + " " + name_split[0].strip()
        name_list.append(name_joined)
    
    party_affiliations = pd.DataFrame({"name": name_list, "party": party_list})
    return party_affiliations    

scrapings = load_html("hansard_scraping.html")
sections = get_sections(scrapings)

stiched_sections = stich_sections(sections)
party_affiliations = load_party_affiliation()

for section in stiched_sections:
    section.extract_details(party_affiliations)

with open("section_data.tsv", "w") as f: 
    f.write("date" + "\t" + "type" + "\t" + "speaker_name" + "\t" + "speaker_party" + "\t" + "content" + "\n")
    for section in stiched_sections:
        f.write(section.section_date + "\t" + section.section_type + "\t" + section.section_speaker + "\t" + section.section_party + "\t" + section.section_content + "\n")