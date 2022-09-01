import os

from pdf_to_text import pdf_to_text
from docx_to_text import docx_to_text
from doc_to_text import doc_to_text
from txt_to_text import txt_to_text

from langdetect import detect
from googletrans import Translator


def prepare_text(file, dolower):
    """
    Takes the resume or any other doc;
    checks the extension of doc and then
    uses suitable methods to extract and
    clean the text
    :param: file :type str
    :return: cleaned tokenized sentences :type list
    """
    reader_choice = {
        ".pdf": pdf_to_text,
        ".docx": docx_to_text,
        ".doc": doc_to_text,
        ".txt": txt_to_text,
    }

    _, ext = os.path.splitext(file)
    try:
        file_content = reader_choice[ext](file, dolower=dolower)
    except KeyError as e:
        return "Could not process files with this extension"
    return file_content
