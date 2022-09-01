from clean_text import clean_text


def txt_to_text(file_path, dolower):
    """
    Extracts plain text from txt files
    :param file_path :type str
    :return:text     :type str
    """
    text = ""
    with open(
        file_path, encoding="unicode_escape", errors="strict", buffering=1
    ) as file:
        data = file.read()
    text += data
    text = clean_text(text, dolower)
    return text
