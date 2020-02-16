rm(list=ls())
getwd()
source("../../parsing_POO_substances.R")
test <- new(Class="Substances","../TXT/index_substances092019.txt")
length(test$substances)
test$retirer_premieres_lignes()
test$substances[1:10]
test$substances <- test$substances[6:length(test$substances)]
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
index_substances092019 <- test$df_decompose
bool <- is.na(index_substances092019$famille)
voir <- subset(index_substances092019,bool)
index_substances092019 <- subset(index_substances092019, !bool)
write.table (index_substances092019, "../CSV/index_substances092019.csv",sep="\t",col.names=T, row.names=F, quote=T)
molecules_seules <- subset (index_substances092019, famille %in% c("Interactions en propre seulement",""))
molecules_seules$famille <- NULL
mol_famille_thesaurus092019 <- subset (index_substances092019, !famille %in% c("Interactions en propre seulement",""))
write.table (molecules_seules, "../CSV/mol_thesaurus_seules092019.csv",sep="\t",col.names=T, row.names=F, quote=T)
write.table (mol_famille_thesaurus092019, "../CSV/mol_famille_thesaurus092019.csv",sep="\t",col.names=T, row.names=F, quote=T)
