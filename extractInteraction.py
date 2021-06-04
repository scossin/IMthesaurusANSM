from python.Interactions.DrugPDDIs import DrugPDDIs
from python.Interactions.Severity_Levels import get_severity_levels_multiple
from python.Interactions.interaction_functions import get_index_first_entry, is_a_line_2_ignore, detect_line_tag, \
    LineTag, check_main_drugs_are_ordered


def writeDebugFile(input_file, lines, step_number):
    debug_filename = __get_debug_file_name(input_file, step_number)
    with open(debug_filename, 'w') as f:
        for line in lines:
            f.write(line)


def __get_debug_file_name(intput_file, step_number):
    debug_filename = intput_file.replace(".txt", "") + "__" + str(step_number) + ".txt"
    return debug_filename


def __pddi_has_multiple_severity_level(pddi):
    multiple_severity_levels = get_severity_levels_multiple()
    names = [severity_level.name for severity_level in multiple_severity_levels]
    return pddi.severity_level in names


if __name__ == "__main__":
    input_file = "R/092019/TXT/thesaurus_092019.txt"
    with open(input_file) as fp:
        DEBUG_MODE = True
        all_lines = fp.readlines()
        index_first_entry = get_index_first_entry(all_lines, "ABATACEPT")
        all_lines = all_lines[index_first_entry:]

        if DEBUG_MODE:
            writeDebugFile(input_file, all_lines, 1)

        lines_filtered = filter(lambda x: not is_a_line_2_ignore(x), all_lines)
        lines_filtered = list(lines_filtered)

        if DEBUG_MODE:
            writeDebugFile(input_file, lines_filtered, 2)

        tags = [detect_line_tag(line) for line in lines_filtered]
        tagged_lines = zip(tags, lines_filtered)
        main_drugs = [line for (tag, line) in tagged_lines
                      if tag == LineTag.MAIN_DRUG]
        if DEBUG_MODE:
            writeDebugFile(input_file, list(main_drugs), 3)
        print(f"checking main_drugs are ordered...")
        check_main_drugs_are_ordered(main_drugs)

        indices_main_drugs = [index for (index, tag) in enumerate(tags)
                              if tag == LineTag.MAIN_DRUG]

        drugPDDIs_list = [None] * len(indices_main_drugs)
        # pddis information about the last main_drug is between its indice and the end of the document
        # So I add here, to indices_main_drugs, the index of the last line
        indices_2_iterate = indices_main_drugs + [len(lines_filtered)]
        for i, index in enumerate(indices_2_iterate[1:]):
            previous_index = indices_2_iterate[i]
            pddi_text = lines_filtered[previous_index:index]
            drugPDDIs_list[i] = DrugPDDIs(pddi_text)

        pddis_list = [[pddi for pddi in drugPDDIs.pddis]
                      for drugPDDIs in drugPDDIs_list]
        pddis = [pddi for pddis in pddis_list for pddi in pddis]  # flatten pddis_list

        pddis_w_several_level = list(filter(__pddi_has_multiple_severity_level, pddis))

        print(f"{len(pddis_w_several_level)} pddis have several severity levels")

        pddis_dict = [pddi.get_dict_representation() for pddi in pddis]

        output_file = "test.json"
        import json

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pddis_dict, f, ensure_ascii=False, indent=4)
        print(f"new file created: {output_file}")

