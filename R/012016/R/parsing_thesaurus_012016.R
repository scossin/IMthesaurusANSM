setRefClass(
  # Nom de la classe
  "Thesaurus2016",

  # Fonctions :
  methods=list(
    ### charge le fichier molécules_seules
    #### spécificités au thesaurus de 2016 : 
    pb_2016_famille_absorbant = function(){
      bool <- thesaurus == "ADSORBANTS"
      bool2 <- grepl("SUBSTANCES A ABSORPTION REDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET",thesaurus)
      if (any(bool | bool2)){
        cat ("problème avec la famille des topiques grastro intestinaux détecté ...  ")
        thesaurus[bool] <- ""
        thesaurus[bool2] <- gsub ("SUBSTANCES A ABSORPTION REDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET ",
                                  "SUBSTANCES A ABSORPTION REDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET ADSORBANTS", thesaurus[bool2])
        bool <- thesaurus == "ADSORBANTS"
        bool2 <- grepl("SUBSTANCES A ABSORPTION REDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET",thesaurus)
        cat ("problème résolu \n")
        thesaurus <<- thesaurus
      } else {
        cat ("aucun problème avec la famille des topiques grastro intestinaux détecté \n")
      }
    }
    ),
  # Set the inheritance for this class
  contains = "Thesaurus"
)