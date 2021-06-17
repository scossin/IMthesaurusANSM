import json
import argparse
from bs4 import BeautifulSoup

from python.Substance.SubstanceDrugClasses import SubstanceClass
from python.Substance.substance_functions import is_a_paragraph_2_ignore, get_index_first_substance


def extract_substance_drug_classes(input_file: str, output_file: str, first_substance: str):
    """
    See help information of main function
    :param input_file:  textual file (.txt)
    :param output_file: json
    :param first_substance: string
    :return: None, write the outputfile
    """
    with open(input_file) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        p_elements = soup.select('.page > p')
        print(f"{len(p_elements)} paragraphs elements detected")

        p_text = [p.get_text() for p in p_elements]

        index_first_substance = get_index_first_substance(p_text, first_substance)
        print(f"first substance: {first_substance} detected at index {index_first_substance}")
        p_text = p_text[index_first_substance:]

        index_2_ignore = list(map(is_a_paragraph_2_ignore, p_text))
        print(f"{sum(index_2_ignore)} empty paragraphs or metadata detected and removed")
        p_text = [text for (text, ignored) in zip(p_text, index_2_ignore) if not ignored]

        substances = [SubstanceClass(text) for text in p_text]
        print(f"{len(substances)} substances detected")
        json_substances = [substance.get_dic_representation() for substance in substances]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_substances, f, ensure_ascii=False, indent=4)
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

    parser.add_argument("-s",
                        "--first_substance",
                        help="the name of the first substance appearing in the document",
                        type=str,
                        required=True
                        )

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

    # first_substance name
    first_substance = args.first_substance

    # extract and output json file
    extract_substance_drug_classes(input_file, output_file, first_substance)
