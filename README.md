# IMthesaurusANSM
Scripts to extract and structure the content of the "thesaurus of drug interactions" published, in a PDF format, by the French Agency for the Safety of Health Products (ANSM) at this address: https://ansm.sante.fr/documents/reference/thesaurus-des-interactions-medicamenteuses-1

## Data
The ANSM interaction working group publishes guidelines once or twice a year. All the files are in the **thesauri** folder.  

## Extraction details

You need to download [tika-app-1.11.jar](https://archive.apache.org/dist/tika/tika-app-1.11.jar):
```bash
wget https://archive.apache.org/dist/tika/tika-app-1.11.jar
```

### Automatic extraction 
```bash
bash extract.sh --help
bash extract.sh -p -t
```
The program creates a TXT folder and a JSON folder in each thesaurus folder. 

### Step by step

First, PDF files are transformed into txt files with Apache Tika.   
For example:
```bash
java -jar tika-app-1.11.jar -h ./thesauri/2019_09/PDF/index_des_substances_09_2019.pdf > ./index_des_substances_09_2019.txt
java -jar tika-app-1.11.jar -t ./thesauri/2019_09/PDF/Thesaurus_09_2019.pdf > 
./Thesaurus_09_2019.txt
```

The message "ERROR FlateFilter: stop reading corrupt stream due to a DataFormatException" can be ignored, the content is correctly extracted. 

Next txt files are transformed to JSON files. For example:
```bash
python extractSubstanceDrugClasses.py -f ./index_substances092019.txt
python extractInteraction.py -f ./thesauri/2019_09/TXT/Thesaurus_09_2019.txt
```

The error message "SeverityLevelerror while extraction PDDI between X and Y" means that the programs has failed to structure the mechanism of action and the severity level of X and Y. To fix this issue, we need to structure it manually and add it to "./python/Interactions/pddis_manually_extracted.json" 

### Tests
Run all the tests with this command: 
```bash
python -m unittest discover ./
```

# Citation 
[Cossin S. Interactions médicamenteuses : données liées et applications. 30 nov 2016.](https://dumas.ccsd.cnrs.fr/dumas-01442668)
