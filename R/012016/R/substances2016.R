####Ce script sert à extraire la liste des médocs du document index_substances.pdf de l'ANSM
source("../../parsing_POO_substances.R")
test <- new(Class="Substances","../TXT/index_substances2016.txt")
length(test$substances)
test$retirer_premieres_lignes()
test$substances_to_df()
nrow(test$df)
test$retirer_lignes_inutiles()
test$retirer_balises()
test$ajout_famille_propre()
test$explose_famille()
test$ajout_parenthese_fermante()
test$pb_gel()

##


index_substances2016 <- test$df_decompose
write.table (index_substances2016, "../CSV/index_substances2016.csv",sep="\t",col.names=T, row.names=F, quote=T)
molecules_seules <- subset (index_substances2016, famille =="Interactions en propre seulement")
molecules_seules$famille <- NULL
mol_famille_thesaurus2016 <- subset (index_substances2016, famille !="Interactions en propre seulement")
write.table (molecules_seules, "../CSV/mol_thesaurus_seules2016.csv",sep="\t",col.names=T, row.names=F, quote=T)
write.table (mol_famille_thesaurus2016, "../CSV/mol_famille_thesaurus2016.csv",sep="\t",col.names=T, row.names=F, quote=T)