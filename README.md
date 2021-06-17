# IMthesaurusANSM
Outils pour extraire le contenu du thesaurus des interactions de l'ANSM et le transformer dans un format réutilisable. [Cossin S. Interactions médicamenteuses : données liées et applications. 30 nov 2016.](https://dumas.ccsd.cnrs.fr/dumas-01442668)

Rpackage to extract the content of the thesaurus of drug interactions publish by the French Agency for the Safety of Health Products (ANSM) at this addresse: https://ansm.sante.fr/documents/reference/thesaurus-des-interactions-medicamenteuses-1

## Data
The ANSM interaction working group publishes guidelines once or twice a year in PDF formats. 
The different versions and their extraction are in the **thesauri** folder.  

## Extraction details
### Extraction script

First, PDF files are transformed into text files with Apache Tika. 
You need to download [tika-app-1.11.jar](https://archive.apache.org/dist/tika/tika-app-1.11.jar) 

```bash
java -jar tika-app-1.11.jar -t Thesaurus_09_2019.pdf > Thesaurus_09_2019.txt
```

Then txt files are transformed to JSON files:
```bash
python extractSubstanceDrugClasses.py  -f R/092019/TXT/index_substances092019.txt -s "abatacept"
```

### Tests
Run all the tests with this command: 
```bash
python -m unittest discover python
```





