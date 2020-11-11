from bs4 import BeautifulSoup
import os
from glob import glob
import re
import json


def citation_conversion(data_folder, file_ext, output_folder):
    """
    This function helps to process all the xml file in the folder
    and convert into single json file for easy access.
    this will strip out the year and court from the xml sentences.

    Parameters
    -----------
    data_folder : str
        The directory in which the xml files are stored.
    file_ext: str
        Extension of the file
    Returns
    ---------
        Result: str
    """
    try:
        citation_name_filtered = []
        citation_tocase_filtered = []

        for path, subdir, files in os.walk(data_folder):
            for file in glob(os.path.join(path, file_ext)):
                with open(file, 'rb') as citation_class_file:
                    soup = BeautifulSoup(citation_class_file, 'xml')

                    # Get citation name
                    citation_name = soup.find_all('name')

                    # Get citation tocase
                    citation_tocase = soup.find_all('tocase')

                    # Get all text in citation
                    for c in citation_name:
                        text = c.text
                        # Removing year and courts from text
                        text = re.sub(r'\([^)]*\)|(\[[^)]*\])|(FCA)|(\d+)',
                                      '', text)
                        text = text.strip()
                        citation_name_filtered.append(text)
                    for c in citation_tocase:
                        text = c.text
                        # Removing year and courts from text
                        text = re.sub(r'\([^)]*\)|(\[[^)]*\])|(\d+)|(FCA)|(;)',
                                      '', text)
                        text = re.sub(r'[ ]{2,}', ' ', text)
                        text = text.strip()
                        text = re.sub(r'[A-Z]{2,}$', '', text)
                        text = text.strip()
                        text = re.sub(r'[A-Z]{2,}$', '', text)
                        text = text.strip()
                        text = re.sub(r'[A-Z]{2,}$', '', text)
                        text = text.strip()
                        citation_tocase_filtered.append(text)
        results = '''All XML File in the folder are processed.
                    Years and court name removed from the sentence
                    '''
        return results
    except Exception as e:
        return str(e)


def fulltext_conversion(data_folder, file_ext, output_folder):
    """
    This function helps to process all the xml file in the folder
    and convert into single json file for easy access.
    this will strip out the year and court from the xml sentences.

    Parameters
    -----------
    data_folder : str
        The directory in which the xml files are stored.
    file_ext: str
        Extension of the file
    output_folder:
        Output folder where json file needs to be saved
    Returns
    ---------
        Result: str
    """
    try:
        full_text = {}
        for path, subdir, files in os.walk(data_folder):
            for file in glob(os.path.join(path, file_ext)):
                with open(file, 'rb') as full_text_file:
                    soup = BeautifulSoup(full_text_file, 'xml')

                    # Get case name
                    case_name = soup.find_all('name')

                    # Get case catchpharse
                    case_catchphrases = soup.find_all('catchphrases')

                    # Get case sentences
                    case_sentences = soup.find_all('sentence')

                    # clean case name
                    for c in case_name:
                        text = c.text
                        # Removing year and courts from text
                        text = re.sub(r'\([^)]*\)|(\[[^)]*\])|(FCA)|(\d+)',
                                      '', text)
                        case_name = text.strip()

                    case_catch_filter = []
                    # clean catchpharse
                    for c in case_catchphrases:
                        text = c.text
                        # Removing ID
                        text = re.sub(r'.*>', '', text)
                        split_text = text.split("\n")
                        for i in split_text:
                            if len(i) > 0:
                                case_catch_filter.append(i)

                    case_sent_filter = []
                    # Clean sentences
                    for c in case_sentences:
                        text = c.text
                        text = text.strip()
                        text = text.strip('.')
                        text = text.lstrip('0123456789.- ')
                        text = re.sub(r'(( [\d])$)|(.*>)|(\n)', '', text)
                        text = text.strip()
                        case_sent_filter.append(text)

                    data = {'case_name': case_name,
                            'catchpharse': case_catch_filter,
                            'full_text': case_sent_filter}

                    full_text[case_name] = data
        with open(output_folder+'/cleaned_full_text.json', 'w') as fp:
            json.dump(full_text, fp)
        results = '''All XML File in the folder are processed.
                    Years and court name removed from the sentence
                    '''
        return results

    except Exception as e:
        return str(e)
