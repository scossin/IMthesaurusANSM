rm(list=ls())
getwd()
source("../../parsing_POO_substances.R")
test <- new(Class="Substances","../TXT/index_substances.txt")
length(test$substances)
test$retirer_premieres_lignes()
test$substances <- test$substances[5:length(test$substances)]
test$substances[1]

substances <- test$substances
test$substances_to_dfplain()
df <- test$df
test$retirer_lignes_inutiles()
test$retirer_balises()

test$ajout_famille_propre()
test$explose_famille()
test$ajout_parenthese_fermante()
test$pb_gel()

##
index_substances2010 <- test$df_decompose
write.table (index_substances2010, "../CSV/index_substances2010.csv",sep="\t",col.names=T, row.names=F, quote=T)
molecules_seules <- subset (index_substances2010, famille =="Interactions en propre seulement")
molecules_seules$famille <- NULL
mol_famille_thesaurus2010 <- subset (index_substances2010, famille !="Interactions en propre seulement")
write.table (molecules_seules, "../CSV/mol_thesaurus_seules2010.csv",sep="\t",col.names=T, row.names=F, quote=T)
write.table (mol_famille_thesaurus2010, "../CSV/mol_famille_thesaurus2010.csv",sep="\t",col.names=T, row.names=F, quote=T)