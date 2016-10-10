#' @noRd
setRefClass(
  # Nom de la classe
  "Substances",
  # Attributs
  fields =  c(
    ### le fichier txt en mémoire :
    substances = "character",

    ## le programme transforme le txt en dataframe à un moment
    df = "data.frame",

    ## le programme ajoute les familles
    df_famille = "data.frame",

    ## certaines molécules ont plusieurs familles
    df_decompose = "data.frame"
  ),

  # Fonctions :
  methods=list(
    ### Constructeur
    initialize = function(fichier_substances_txt){
      ### library :
      library(stringr)
      substances <<- readLines(fichier_substances_txt)

    },

    retirer_premieres_lignes = function(){
      bool <- grepl ("Mise à jour",substances)
      ligne_mise_a_jour <- which(bool)
      print (substances[1:which(bool)])
      substances <<- substances[which(bool):length(substances)]
      cat ("les lignes ci-dessus ont été retirées")
      },

    substances_to_df = function(){
      regex_balise <- "<p>"
      bool <- grepl (regex_balise, substances)
      lignes_p <- which(bool)
      lignes_merges <- c()
      for (i in 1:(length(lignes_p))){
        ### gérer le dernier cas :
        if (lignes_p[i] == max(lignes_p)){
          lignes_a_merge <- (lignes_p[i]+1):length(substances)
        } else {
          lignes_a_merge <- (lignes_p[i]+1):(lignes_p[i+1]-1)
        }
        temp <- paste (substances[lignes_a_merge], collapse="")
        lignes_merges <- append(lignes_merges, temp)
      }
      df <<- data.frame (entites = substances[bool], medocs = lignes_merges)
    },
    retirer_lignes_inutiles = function(){
      regex_maj <- "Mise à jour"
      regex_site <- "www.ansm.sante.fr"
      regex_ANSM <- "^<p>ANSM "
      regex <- c(regex_maj,regex_site,regex_ANSM)
      for (i in regex){
        bool <- grepl(i, df$entites)
        cat (sum(bool), "lignes contenant", i, "retirées \n")
        df <<- subset (df, !bool)
      }
    },


    retirer_balises = function(){
      cleanFun = function(htmlString) {
        return(gsub("<.*?>", "", htmlString))
      }
      df$medocs <<- sapply(df$medocs, cleanFun)
      df$entites <<- sapply(df$entites, cleanFun)
      df$medocs <<- gsub ("^\\(","",df$medocs)
      df$medocs <<- gsub ("\\)$","",df$medocs)
      df$medocs <<- gsub ("^ ", "",df$medocs)
      cat ("les balises ont été retirés des libellés")
    },

    ajout_famille_propre = function(){
      regex_famille <- "(^Voir :)|(^Interactions en propre mais voir aussi : )"
      bool <- grepl(regex_famille, df$medocs)
      cat(sum(bool), "molécules sont rattachées à une famille \n")
      df_famille <<- df
      df_famille$medocs <<- gsub ("^Voir : ","",df_famille$medocs)
      df_famille$medocs <<- gsub ("^Interactions en propre mais voir aussi : ","",df_famille$medocs)
      regex_propre <- "^Interactions en propre seulement$"
      bool2 <- grepl(regex_propre, df_famille$medocs)
      cat(sum(bool2), "molécules en interaction propre \n")
      df_famille$famille <<- ifelse (bool, df_famille$medocs,
                            ifelse (bool2, df_famille$medocs,NA))
      if (sum(is.na(df_famille$famille)) != 0){
        voir <- subset (df_famille, is.na(df_famille$famille))
        print (voir)
        stop("Certaines molécules ne sont pas rattachées à une famille ni interaction en propre \n")
      }

      ## 2013 : Interactions en propre mais voir aussi : et rien après
      bool <- df_famille$famille == ""
      df_famille$famille[bool] <<- "Interactions en propre seulement"

      df_famille <<- df_famille
    },

    explose_famille = function(){
      ## certaines molécules ont plusieurs familles séparées par -
      cat(nrow(df_famille), "lignes dans la df avant explosion \n")
      nombres_rep <- unlist(lapply (str_split(df_famille$famille," - "), length))
      nom_entite <- c()
      for (i in 1:length(nombres_rep)){
        nom_entite <- append (nom_entite, rep(df_famille$entites[i], nombres_rep[i]))
      }
      nom_medocs <- unlist(str_split(df_famille$famille," - "))
      if (length(nom_medocs) == length(nom_entite)){
        df_explose <- data.frame (entites=nom_entite, medocs=nom_medocs)
        df_explose$medocs <- gsub ("^ ","",df_explose$medocs)
      } else {
        stop ("Probleme pour exploser les médocs")
      }
      colnames(df_explose) <- c("molecule","famille")
      cat(nrow(df_explose), "lignes dans la df_decompose \n")
      df_decompose <<- df_explose
    },

    explose_molecule = function(){
      cat(nrow(df), "lignes dans la df avant explosion \n")
      nombres_rep <- unlist(lapply (str_split(df$medocs,","), length))
      nom_entite <- c()
      for (i in 1:length(nombres_rep)){
        nom_entite <- append (nom_entite, rep(df$entites[i], nombres_rep[i]))
      }
      nom_medocs <- unlist(str_split(df$medocs,","))
      if (length(nom_medocs) == length(nom_entite)){
        df_explose <- data.frame (entites=nom_entite, medocs=nom_medocs)
        df_explose$medocs <- gsub ("^ ","",df_explose$medocs)
      } else {
        stop ("Probleme pour exploser les médocs")
      }
      cat(nrow(df_explose), "lignes dans la df après explosion \n")
      colnames(df_explose) <- c("famille","molecule")
      df_decompose <<- df_explose
      df_decompose$famille <<- as.character(df_decompose$famille)
      df_decompose$molecule <<- as.character(df_decompose$molecule)
    },

    ajout_parenthese_fermante = function(){
      bool <- grepl("\\(", df_decompose$famille) & !grepl("\\)", df_decompose$famille)
      cat(sum(bool), "parenthèses fermantes ajoutées \n")
      df_decompose$famille[bool] <<- paste (df_decompose$famille[bool], ")",sep="")
    },

    pb_gel = function(){
      bool <- grepl ("gel d'hydroxyde d'aluminium et de carbonate de magnesium$", df_decompose$molecule)
      cat (sum(bool), "gel d'hydroxyde d'aluminium et de carbonate de magnesium", "remplacé par",
           "\n gel d'hydroxyde d'aluminium et de carbonate de magnesium codesseches \n")
      df_decompose$molecule <<- as.character(df_decompose$molecule)
      df_decompose$molecule[bool] <<- "gel d'hydroxyde d'aluminium et de carbonate de magnesium codesseches"
    },

    ### parfois le format strucutré n'est pas identique ..
    ## donc il faut passer en plain text et utiliser cette fonction de transformation
    substances_to_dfplain=function(){
      substances2 <- c()
      counter <- 0
      ### fusionner les descriptions sur plusieurs lignes
      for (i in substances){
        premierC <- substr(i,1,4)
        if (i != "" & counter == 1){
          dernier <- substances2[length(substances2)]
          dernier_ajout <- paste(dernier, i, sep="")
          substances2[length(substances2)] <- dernier_ajout
        } else {
          substances2 <- append(substances2, i)
          counter <- 0
        }

        if (premierC %in% c("Voir","Inte")){
          counter <- 1
        }
      }

      substances3 <- c()
      counter<- 0
      for (i in substances2){
        if (counter == 1 & i == ""){
          next
        }
        if (i == ""){
          counter <- 1
        } else {
          counter <- 0
        }
        substances3 <- append (substances3, i)
      }
      matrice <- matrix(substances3,ncol = 4, byrow = T)
      matrice <- as.data.frame(matrice)
      matrice$V2 <- NULL
      matrice$V4 <- NULL
      colnames(matrice) <- c("entites","medocs")
      df <<- matrice
    }
  ),
)
