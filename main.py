import sys
import json
import warnings
from parser import Parser

warnings.filterwarnings("ignore")

sys.path.append("./datareader")
from prepare_text import prepare_text

from resume_segmenter import ResumeSegmenter

test_resume_path = "inputdata/Ali, Mohammad_Taha - 2022-06-23 07-36-29.pdf"

resume_lines = prepare_text(test_resume_path, dolower=True)

print(resume_lines)

with open("resume_parsed_info.txt", "w") as outfile:
    outfile.write(resume_lines)

segmenter = ResumeSegmenter()
resume_segments = segmenter.segment(resume_lines)

with open('segment_data.json', 'w', encoding='utf-8') as f:
    json.dump(resume_segments, f, ensure_ascii=False, indent=4)

parser_obj = Parser()
parsed_information = parser_obj.segmentResume(resume_lines)

with open("parsed_information.json", "w") as outfile:
    json.dump(parsed_information, outfile, indent=4)

email_and_phone = parser_obj.profile_information_parser(resume_lines)

with open("email_and_phone.json", "w") as outfile:
    json.dump(email_and_phone, outfile, indent=4)