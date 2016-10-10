##### Parsing le thesaurus de juin 2015
source("../../parsing_POO_thesaurus.R")

test <- new(Class = "Thesaurus",fichier_thesaurus_txt = "../TXT/thesaurus_2015.txt",
            fichier_mol_seules_csv = "../CSV/mol_thesaurus_seules2015.csv"
            ,fichier_mol_famille_csv="../CSV/mol_famille_thesaurus2015.csv")

length(test$thesaurus)

## num page
test$retirer_num_page()
## espace :
test$retirer_espace()
## retirer les accents
test$retirer_accent()
## certaines lignes sont seules :
test$retirer_bas_de_page("^ANSM")
test$retirer_bas_de_page("Interactions medicamenteuses - Thesaurus")
test$retirer_bas_de_page("www.ansm.sante.fr [0-9]+")
##
test$retirer_premieres_lignes()
##
test$set_lignes_entrees()
test$lignes_entrees
##
test$verif_entrees()
test$pb_2015_faute_racecadodril()
test$verif_entrees2()

test$thesaurus[test$lignes_entrees]

test$remove_entrees(nom_entree = "ANTI-INFECTIEUX ET INR")
test$verif_entrees2()

## df :
test$thesaurus_to_df()
nrow(test$df)
test$add_mecanisme_explication()
test$verif_interaction()
test$retire_AUTRES()
test$verif_interaction()
test$retire_MEDICAMENTS()
test$verif_interaction()
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
test$check_decompose()

thesaurus062015 <- test
save(thesaurus062015, file="../../../data/thesaurus062015.rdata")


### suprpimer : 
test$fichier_thesaurus_txt
df <- test$df
test$fichier_mol_seules_csv
test$fichier_mol_famille_csv
voir <- test$molecules_seules
