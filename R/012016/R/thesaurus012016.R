# classe parente
library(methods)
source("../../parsing_POO_thesaurus.R")

fichier_thesaurus_txt = "../TXT/thesaurus_2016.txt"
fichier_mol_seules_csv = "../CSV/mol_thesaurus_seules2016.csv"
fichier_mol_famille_csv = "../CSV/mol_famille_thesaurus2016.csv"

test <- new(Class = "Thesaurus",fichier_thesaurus_txt = fichier_thesaurus_txt,
            fichier_mol_seules_csv = fichier_mol_seules_csv
            ,fichier_mol_famille_csv=fichier_mol_famille_csv)


length(test$thesaurus)
test$retirer_premieres_lignes()
### nombre de pages à diminuer
length(test$thesaurus)
## la répétition ne modifie pas :
test$retirer_premieres_lignes()
## num page
test$retirer_num_page()
test$retirer_num_page()

## espace :
test$retirer_espace()
test$retirer_espace()

## retirer les accents
test$retirer_accent()


## certaines lignes sont seules :
test$retirer_bas_de_page("^ANSM")
test$retirer_bas_de_page("Interactions medicamenteuses - Thesaurus")
test$retirer_bas_de_page("www.ansm.sante.fr [0-9]+")

##
test$pb_2016_famille_absorbant()

##
test$lignes_entrees
test$set_lignes_entrees()

##
test$verif_entrees()

test$verif_entrees2()

test$thesaurus[test$lignes_entrees]

test$remove_entrees(nom_entree = "ANTI-INFECTIEUX ET INR")

## df :
test$thesaurus_to_df()
nrow(test$df)

test$add_mecanisme_explication()

test$verif_interaction()

test$retire_AUTRES()

test$verif_interaction()

test$retire_MEDICAMENTS()

test$verif_mol_famille()

test$verif_famille_entrees()

test$contenu_description_hors_molecules()


test$replace_il_convient()

test$classifie_niveau()

voir <- test$verif_absence_de_niveau()

df <- test$df
test$df_sans_doublon()
df <- test$df
test$set_df_decompose()
test$create_manuellement()
nrow(test$manuellement)
thesaurus012016 <- test
save(thesaurus012016, file="../../../data/thesaurus012016.rdata")
