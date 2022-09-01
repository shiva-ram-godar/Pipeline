from clean_text import clean_text
from subprocess import Popen, PIPE


def doc_to_text(filepath, dolower):
    """
    Takes the doc file from the
    file path param and returns
    the cleaned the text from the
    file.
    :param filepath: path/directory of the doc file in the system
    :return: Returns the cleaned text from the file
    """
    text = ""
    cmd = ["antiword", filepath]
    p = Popen(cmd, stdout=PIPE)
    stdout, stderr = p.communicate()
    text += stdout.decode("utf-8", "ignore")
    text = clean_text(text, dolower)
    return text
