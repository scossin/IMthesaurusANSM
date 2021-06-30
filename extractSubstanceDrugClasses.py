import json
import argparse
from typing import List

from bs4 import BeautifulSoup

from python.Interactions.PDDIobject import SubstanceObject
from python.Interactions.interaction_functions import get_index_first_entry
from python.Substance.SubstanceDrugClasses import SubstanceClass
from python.Substance.substance_functions import is_a_paragraph_2_ignore, remove_wrong_p_tag, \
    fix_specific_lines_before_extraction
from python.Substance.AltDrugClassLabels import AltDrugClassLabels


def extract_substance_drug_classes(input_file: str, output_file: str, debug_mode=False):
    """
    See help information of main function
    :param debug_mode:
    :param input_file:  textual file (.txt)
    :param output_file: json
    :return: None, write the outputfile
    """
    with open(input_file) as fp:
        all_lines = fp.readlines()
        # in old substances versions, Tika extraction is different so we need to remove some <p> and </p> tags here
        remove_wrong_p_tag(all_lines)

        all_lines = [fix_specific_lines_before_extraction(line) for line in all_lines]

        soup = BeautifulSoup("".join(all_lines), "html.parser")
        p_elements = soup.select('.page > p')

        if debug_mode:
            print(f"{len(p_elements)} paragraphs elements detected")

        p_text = [p.get_text() for p in p_elements]

        index_first_substance = get_index_first_entry(p_text)
        if debug_mode:
            print(f"first substance detected at index {index_first_substance}")
        p_text = p_text[index_first_substance:]

        index_2_ignore = list(map(is_a_paragraph_2_ignore, p_text))
        if debug_mode:
            print(f"{sum(index_2_ignore)} empty paragraphs or metadata detected and removed")
        p_text = [text for (text, ignored) in zip(p_text, index_2_ignore) if not ignored]

        substances = [SubstanceClass(text) for text in p_text]
        if debug_mode:
            print(f"{len(substances)} substances detected")
        sub_objects: List[SubstanceObject] = [substance.get_substance_object() for substance in substances]

        # There are missing drug classes labels in the substance file
        # for example substance in the class "retinoides" are also in the class "autres retinoides"
        # we add this information here:
        [AltDrugClassLabels().add_alternative_class_labels(substance_object) for substance_object in sub_objects]

        dict_representations = [substance_object.dict() for substance_object in sub_objects]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dict_representations, f, ensure_ascii=False, indent=4)
        if debug_mode:
            print(f"new file created: {output_file}")


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='Extract substances and their drugs classes '
                                                 'from the textual content of a PDF document "index des substances" .')

    parser.add_argument("-f",
                        "--filename",
                        help="the path to the textual file (.txt) containing substances and drug classes to extract",
                        type=str,
                        required=True)

    parser.add_argument("-o",
                        "--outputfile",
                        help="the path to the json output file",
                        type=str)

    parser.add_argument("--debug_mode",
                        help="whether to write intermediate files during the several steps of extraction",
                        type=str)

    args = parser.parse_args()

    # inputfile
    if not args.filename.endswith(".txt"):
        raise ValueError("argument error: filename must end by txt")
    input_file = args.filename

    # outputfile
    if not args.outputfile:
        output_file = input_file.replace(".txt", ".json")
    else:
        output_file = args.outputfile

    # debug_mode
    if not args.debug_mode:
        debug_mode = False
    else:
        debug_mode = True

    # extract and output json file
    extract_substance_drug_classes(input_file, output_file, debug_mode)
