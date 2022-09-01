import docx2txt
from clean_text import clean_text


def docx_to_text(file_path, dolower):
    """
    Takes docx files and
    extracts plain text
    from the docx files
    :param file_path :type str
    :return:text     :type str
    """
    text = ""
    text += docx2txt.process(file_path)
    text = clean_text(text, dolower)
    return text
