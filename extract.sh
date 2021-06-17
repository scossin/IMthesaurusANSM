#! /bin/bash
currentDir=$(dirname "$(realpath $0)")

is_thesaurus_file () {
    base=$(basename "$1")
    if [[ $base == *"thesaurus"* ]] || [[ $base == *"Thesaurus"* ]] ; then
        return 0 # true
    fi
    return 1 # false
}

create_folder_if_not_exists () {
    txt_folder=$1
    if [ ! -d $txt_folder ]; then
        mkdir $txt_folder
    fi
}

extract_pdf_thesaurus () {
    thesaurus_file=$1
    output_file=$2
    commande="java -jar tika-app-1.11.jar -t $thesaurus_file > $output_file"
    echo $commande
    eval $commande
}

# PDF -> TXT
# for folder in $currentDir/thesauri/*; do
#     if [ -d $folder ]; then
#         for filename in $folder/PDF/*.pdf; do
#             if is_thesaurus_file "$filename"; then
#                 txt_folder=$folder/TXT
#                 create_folder_if_not_exists $txt_folder
#                 base=$(basename "$filename")
#                 txt_filename=${base/pdf/txt}
#                 txt_file=$(echo $txt_folder/$txt_filename)
#                 extract_pdf_thesaurus $filename $txt_file
#             fi 
#         done
#     fi
# done

structure_thesaurus () {
    txt_file=$1
    output_file=$2
    commande="python extractInteraction.py  -f $txt_file -o $output_file"
    echo $commande
    eval $commande
}

# TXT -> JSON
for folder in $currentDir/thesauri/*; do
    if [ -d $folder ]; then
        for filename in $folder/TXT/*.txt; do
            if is_thesaurus_file "$filename"; then
                json_folder=$folder/JSON
                create_folder_if_not_exists $json_folder
                base=$(basename "$filename")
                json_filename=${base/txt/json}
                json_file=$(echo $json_folder/$json_filename)
                structure_thesaurus $filename $json_file
            fi 
        done
    fi
done

