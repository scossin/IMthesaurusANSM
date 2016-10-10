source("../../parsing_POO_substances.R")
test <- new(Class="Substances","../TXT/index_classes2016.txt")
length(test$substances)
test$retirer_premieres_lignes()
test$substances_to_df()
nrow(test$df)
voir <- test$df
test$retirer_lignes_inutiles()
test$retirer_balises()
#test$ajout_famille_propre()
test$explose_molecule()

