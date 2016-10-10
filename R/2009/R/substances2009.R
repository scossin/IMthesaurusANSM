####Ce script sert à extraire la liste des médocs du document index_substances.pdf de l'ANSM
## script parsing 2016 :
rm(list=ls())
getwd()
source("../../parsing_POO_substances.R")
test <- new(Class="Substances","../TXT/index_substances2009.txt")
length(test$substances)
test$retirer_premieres_lignes()
test$substances[1:10]
test$substances <- test$substances[2:length(test$substances)]
test$substances[1]

test$substances_to_df()
df <- test$df
test$retirer_lignes_inutiles()
test$retirer_balises()

test$ajout_famille_propre()
test$explose_famille()
test$ajout_parenthese_fermante()
test$pb_gel()

##
index_substances2009 <- test$df_decompose
write.table (index_substances2009, "../CSV/index_substances2009.csv",sep="\t",col.names=T, row.names=F, quote=T)
molecules_seules <- subset (index_substances2009, famille =="Interactions en propre seulement")
molecules_seules$famille <- NULL
mol_famille_thesaurus2009 <- subset (index_substances2009, famille !="Interactions en propre seulement")
write.table (molecules_seules, "../CSV/mol_thesaurus_seules2009.csv",sep="\t",col.names=T, row.names=F, quote=T)
write.table (mol_famille_thesaurus2009, "../CSV/mol_famille_thesaurus2009.csv",sep="\t",col.names=T, row.names=F, quote=T)

