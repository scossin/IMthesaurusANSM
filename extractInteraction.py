import argparse
import json

from python.Interactions.DrugPDDIs import DrugPDDIs
from python.Interactions.interaction_functions import get_index_first_entry, is_a_line_2_ignore, detect_line_tag, \
    LineTag, check_main_drugs_are_ordered, fix_specific_lines_before_extraction


def writeDebugFile(input_file, lines, step_number):
    debug_filename = __get_debug_file_name(input_file, step_number)
    with open(debug_filename, 'w') as f:
        for line in lines:
            f.write(line)


def __get_debug_file_name(intput_file, step_number):
    debug_filename = intput_file.replace(".txt", "") + "__" + str(step_number) + ".txt"
    return debug_filename


def extract_pddis(lines: list, debug_mode=False) -> list:
    if debug_mode:
        writeDebugFile(input_file, lines, 1)

    lines_fixed = list(map(fix_specific_lines_before_extraction, lines))
    if debug_mode:
        writeDebugFile(input_file, lines_fixed, 1.1)

    lines_filtered = filter(lambda x: not is_a_line_2_ignore(x), lines_fixed)
    lines_filtered = list(lines_filtered)

    if debug_mode:
        writeDebugFile(input_file, lines_filtered, 2)

    tags = [detect_line_tag(line) for line in lines_filtered]
    tagged_lines = zip(tags, lines_filtered)
    main_drugs = [line for (tag, line) in tagged_lines
                  if tag == LineTag.MAIN_DRUG]
    if debug_mode:
        writeDebugFile(input_file, list(main_drugs), 3)
    print(f"checking main_drugs are ordered...")
    check_main_drugs_are_ordered(main_drugs)

    indices_main_drugs = [index for (index, tag) in enumerate(tags)
                          if tag == LineTag.MAIN_DRUG]

    drug_pddis_list = [None] * len(indices_main_drugs)
    # pddis information about the last main_drug is between its indice and the end of the document
    # So I add here, to indices_main_drugs, the index of the last line
    indices_2_iterate = indices_main_drugs + [len(lines_filtered)]
    for i, index in enumerate(indices_2_iterate[1:]):
        previous_index = indices_2_iterate[i]
        pddi_text = lines_filtered[previous_index:index]
        drug_pddis_list[i] = DrugPDDIs(pddi_text)

    pddis_list = [[pddi for pddi in drugPDDIs.pddis]
                  for drugPDDIs in drug_pddis_list]
    pddis = [pddi for pddis in pddis_list for pddi in pddis]  # flatten pddis_list
    return pddis


if __name__ == "__main__":
    # python extractInteraction.py -f "R/092019/TXT/thesaurus_092019.txt"

    # parse arguments
    parser = argparse.ArgumentParser(description='Extract potential drug drug interactions '
                                                 'from the textual content of a PDF document "thesaurus des interactions".')

    parser.add_argument("-f",
                        "--filename",
                        help="the path to the textual file (.txt) containing potential drug drug interactions",
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
        debug_mode = True
    else:
        debug_mode = False

    with open(input_file) as fp:
        all_lines = fp.readlines()
        index_first_entry = get_index_first_entry(all_lines, "ABATACEPT")
        all_lines = all_lines[index_first_entry:]

        pddis = extract_pddis(all_lines, debug_mode)

        pddis_dict = [pddi.get_dict_representation() for pddi in pddis]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pddis_dict, f, ensure_ascii=False, indent=4)
        print(f"new file created: {output_file}")
