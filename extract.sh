#! /bin/bash

print_help () {
   # Display Help
   echo "Extraction script."
   echo
   echo "options:"
   echo "p     Extract PDF files to TXT files (TXT folder is automatically created)"
   echo "t     Extraction TXT files to JSON files (JSON folder is automatically created)"
   echo "r     Remove TXT and JSON folder"
   exit 0
}

while :; do
    case $1 in
        -h|--help) print_help        
        ;;
        -p|--pdf) extractPDF="SET"            
        ;;
        -t|--txt) extractTXT="SET"            
        ;;
        -r|--remove) removeTXTandJSONfolders="SET"            
        ;;
        *) break
    esac
    shift
done



currentDir=$(dirname "$(realpath $0)")

is_thesaurus_file () {
    base=$(basename "$1")
    if [[ $base == *"thesaurus"* ]] || [[ $base == *"Thesaurus"* ]] ; then
        return 0 # true
    fi
    return 1 # false
}

is_substance_file () {
    base=$(basename "$1")
    if [[ $base == *"substance"* ]] || [[ $base == *"Substances"* ]] ; then
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

extract_pdf_substance () {
    substance_file=$1
    output_file=$2
    commande="java -jar tika-app-1.11.jar -h $substance_file > $output_file"
    echo $commande
    eval $commande
}

if [ $removeTXTandJSONfolders ]; then
    for folder in $currentDir/thesauri/*; do
        if [ -d $folder ]; then
            txt_folder=$folder/TXT
            create_folder_if_not_exists $txt_folder
            echo "Removing $folder/TXT"
            rm -R $folder/TXT
            echo "Removing $folder/JSON"
            rm -R $folder/JSON
            continue
        fi
    done 
fi

# PDF -> TXT
if [ $extractPDF ]; then
    echo "Extracting PDF files to TXT..."
    for folder in $currentDir/thesauri/*; do
        if [ -d $folder ]; then
            txt_folder=$folder/TXT
            create_folder_if_not_exists $txt_folder
            for filename in $folder/PDF/*.pdf; do
                base=$(basename "$filename")
                txt_filename=${base/pdf/txt}
                txt_file=$(echo $txt_folder/$txt_filename)
                if is_thesaurus_file "$filename"; then
                    extract_pdf_thesaurus $filename $txt_file
                elif is_substance_file "$filename"; then
                    extract_pdf_substance $filename $txt_file
                fi
            done
        fi
    done
fi 

thesaurus_txt_2_json () {
    txt_file=$1
    output_file=$2
    commande="python extractInteraction.py  -f $txt_file -o $output_file"
    echo $commande
    eval $commande
}

substances_txt_2_json () {
    txt_file=$1
    output_file=$2
    commande="python extractSubstanceDrugClasses.py  -f $txt_file -o $output_file"
    echo $commande
    eval $commande
}

# TXT -> JSON
if [ $extractTXT ]; then
    for folder in $currentDir/thesauri/*; do
        if [ -d $folder ]; then
            for filename in $folder/TXT/*.txt; do
                json_folder=$folder/JSON
                create_folder_if_not_exists $json_folder
                base=$(basename "$filename")
                json_filename=${base/txt/json}
                json_file=$(echo $json_folder/$json_filename)
                if is_thesaurus_file "$filename"; then   
                    thesaurus_txt_2_json $filename $json_file
                elif is_substance_file "$filename"; then   
                    substances_txt_2_json $filename $json_file
                fi  
            done
        fi
    done
fi
