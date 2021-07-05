# IMthesaurusANSM (DEPRECATED - See https://github.com/scossin/ExtractThesaurusANSM)
Paquet R développé pour extraire le PDF du thesaurus des interactions de l'ANSM et le transformer dans un format structuré (R dataframe). [Cossin S. Interactions médicamenteuses : données liées et applications. 30 nov 2016.](https://dumas.ccsd.cnrs.fr/dumas-01442668)

Rpackage to extract the content of the thesaurus of drug interactions edited by ANSM (french national drug safety institute)

## installation
To get the current development version from github:
```R
# install.packages("devtools")
devtools::install_github("scossin/IMthesaurusANSM")
```

## How it works
In the R folder, you'll find the extraction programs of the PDF thesaurus since 2009.
PDF files are transformed into text files with the tool Apache Tika version 1.1. 
Then a Rscript per thesaurus transforms text files into Rdataframe (all are in the data folder). 
All Rscripts use the same class : "parsing_POO_thesaurus.R".

## CSV files
If you are not familiar with R, you may need to transform Rdataframe into CSV files. 
see "exampleThesaurusToCSV.R" file
