####Ce script sert à extraire la liste des médocs du document index_substances.pdf de l'ANSM
source("../../parsing_POO_substances.R")
test <- new(Class="Substances","../TXT/index_substances2013.txt")
length(test$substances)
test$retirer_premieres_lignes()
test$substances_to_df()
voir <- test$df
nrow(test$df)
df <- test$df
test$retirer_lignes_inutiles()
test$retirer_balises()
test$ajout_famille_propre()
test$explose_famille()
test$ajout_parenthese_fermante()
test$pb_gel()
voir <- test$df_famille
##

index_substances2013 <- test$df_decompose
write.table (index_substances2013, "../CSV/index_substances2013.csv",sep="\t",col.names=T, row.names=F, quote=T)
molecules_seules <- subset (index_substances2013, famille =="Interactions en propre seulement")
molecules_seules$famille <- NULL
mol_famille_thesaurus2013 <- subset (index_substances2013, famille !="Interactions en propre seulement")
write.table (molecules_seules, "../CSV/mol_thesaurus_seules2013.csv",sep="\t",col.names=T, row.names=F, quote=T)
write.table (mol_famille_thesaurus2013, "../CSV/mol_famille_thesaurus2013.csv",sep="\t",col.names=T, row.names=F, quote=T)
