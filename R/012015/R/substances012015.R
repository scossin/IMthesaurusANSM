####Ce script sert à extraire la liste des médocs du document index_substances.pdf de l'ANSM
rm(list=ls())
getwd()
source("../../parsing_POO_substances.R")
test <- new(Class="Substances","../TXT/index_substances012015.txt")
length(test$substances)
test$retirer_premieres_lignes()
test$substances[1:10]
test$substances <- test$substances[9:length(test$substances)]
test$substances[1]

## retirer pages : 
bool <- grepl("^Page",test$substances)
any(bool)
test$substances[bool]
test$substances[bool] <- ""

test$substances_to_dfplain()
df <- test$df
test$retirer_lignes_inutiles()
test$retirer_balises()

test$ajout_famille_propre()
test$explose_famille()
test$ajout_parenthese_fermante()
test$pb_gel()

##
index_substances012015 <- test$df_decompose
write.table (index_substances012015, "../CSV/index_substances012015.csv",sep="\t",col.names=T, row.names=F, quote=T)
molecules_seules <- subset (index_substances012015, famille =="Interactions en propre seulement")
molecules_seules$famille <- NULL
mol_famille_thesaurus012015 <- subset (index_substances012015, famille !="Interactions en propre seulement")
write.table (molecules_seules, "../CSV/mol_thesaurus_seules012015.csv",sep="\t",col.names=T, row.names=F, quote=T)
write.table (mol_famille_thesaurus012015, "../CSV/mol_famille_thesaurus012015.csv",sep="\t",col.names=T, row.names=F, quote=T)