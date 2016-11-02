#' @title A Reference Class pour extraire le contenu du thesaurus des interactions de l'ANSM
#' @name Thesaurus
#' @description Cette classe est utilisée pour transformer le contenu textuel (plain text obtenu par l'outil Tika à partir du PDF) du thésaurus
#' en contenu structuré (dataframe R).
#' @field thesaurus : le contenu du thesaurus en texte brut
#' @field lignes_entrees : numéros des lignes où on trouvent une entrée
#' @field regex_exclus : si ces lignes commencent par ces regex, ce ne sont pas des entrées (ECG...)
#' @field df : dataframe contenant la liste des protagoniste A - B du thesaurus avec la description, le mécanisme et le niveau
#' @field df_decompose : pareil que df mais les familles sont remplacées par les molécules qu'elles contiennent
#' @field manuellement : subset de df où il existe plusieurs niveaux d'interaction selon le contexte.
#' L'idée est de traiter manuellement cette partie pour séparer les niveaux puis l'intégrer à df.
#' @field mol_famille : dataframe contenant les molécules et leurs familles.
#' @field molecules_seules : dataframe contenant la liste des molécules seules.
#' @field mol : vecteur contenant la liste des molécules du thésaurus
#' @details Les fonctions servent à transformer le contenu du thesaurus d'un format textuel à un format structuré.
#' Elles n'ont pas d'utilité par la suite
#' @return Permet de créer des instances de cette classe contenant diverses informations sur une mise à jour-thésaurus
setRefClass(
  # Nom de la classe
  "Thesaurus",
  # Attributs
  fields =  c(
    ### le fichier txt en mémoire :
    thesaurus = "character",
    ### lignes contenant les entrées du thésaurus :
    lignes_entrees = "numeric",
    ### si ces lignes commencent par ces regex, ce ne sont pas des entrées
    regex_exclus = "character",

    ## le programme transforme le txt en dataframe à un moment
    df = "data.frame",

    ## remplace les familles par les molécules
    df_decompose = "data.frame",

    ## certaines interactions ont plusieurs interactions qu'il faut modifier manuellement :
    manuellement = "data.frame",

    ## les 2 autres fichiers accompagnant le thesaurus
    molecules_seules = "ANY",

    ##
    mol_famille ="ANY",

    ## mol : contient toutes les molécules du thésaurus
    mol = "character"
  ),

  # Fonctions :
  methods=list(
    ### Constructeur
    initialize = function(fichier_thesaurus_txt,fichier_mol_seules_csv = NULL,fichier_mol_famille_csv= NULL){
        ### library :
        library(stringr)

        regex_exclus <<- "^CONTRE-INDICATION|^ECG |^CI |^ASDEC |^PE |^CYP3A4|[a-z]+"

        thesaurus <<- readLines (fichier_thesaurus_txt)

        if (!is.null(fichier_mol_seules_csv)){
          load_fichier_mol_seules_csv(fichier_mol_seules_csv)
        }

        if (!is.null(fichier_mol_famille_csv)){
          load_fichier_mol_famille_csv(fichier_mol_famille_csv)
        }

      },

    ### charge le fichier molécules_seules
    load_fichier_mol_seules_csv = function(fichier_mol_seules_csv){
      molecules_seules <<- read.table (fichier_mol_seules_csv,sep="\t",header=T)
      if (any(!all(colnames(molecules_seules) %in% c("molecule","famille")))){
        stop("Erreur, molecules_seules ne contient pas les bonnes colonnes")
      }
      molecules_seules$molecule <<- iconv(molecules_seules$molecule, to='ASCII//TRANSLIT')
      molecules_seules$molecule  <<- toupper(molecules_seules$molecule)
    },

    load_fichier_mol_famille_csv = function(fichier_mol_famille_csv){
      mol_famille <<- read.table (fichier_mol_famille_csv,sep="\t",header=T)
      if (any(!all(colnames(mol_famille) %in% c("molecule","famille")))){
        stop("Erreur, mol_famille ne contient pas les bonnes colonnes")
      }
      mol_famille$molecule <<- iconv(mol_famille$molecule, to='ASCII//TRANSLIT')
      mol_famille$famille <<- iconv(mol_famille$famille, to='ASCII//TRANSLIT')
      mol_famille$molecule  <<- toupper(mol_famille$molecule )
      mol_famille$famille <<- toupper(mol_famille$famille )

      ### molecules du thesaurus :
      mol <<- unique(c(mol_famille$molecule, molecules_seules$molecule))
    },

    ### les fonctions sont dans l'ordre de leur utilisation
    retirer_premieres_lignes = function(){
      premiere_entree <- "[A-Z]{2,}"
      bool <- grepl(premiere_entree, thesaurus)
      ligne_premiere_entree <- min(which(as.numeric(bool) == 1))
      cat("premiere entree détectée : ",thesaurus[ligne_premiere_entree],"
      suppression des lignes avant cette entrée : ")
      thesaurus <<- thesaurus[ligne_premiere_entree:length(thesaurus)]
      cat("OK \n")
    },

    ### les numéros sont seuls sur une ligne et correspondent au bas de page du document PDF
    retirer_num_page = function(){
      regex_chiffre_seul <- "^[0-9]{1,3}$"
      bool <- grepl (regex_chiffre_seul, thesaurus)
      cat (length(thesaurus[bool]), " numéros de pages détectés et retirés \n")
      thesaurus[bool] <<- ""
    },



    retirer_bas_de_page = function(regex){
      bool <- grepl(regex,thesaurus)
      if (any(bool)){
        cat (sum(bool), "\"", unique(thesaurus[bool]),"\"supprimés \n")
        thesaurus[bool] <<- ""
      } else {
        cat (regex, "non détecté \n")
      }
    },

    retirer_espace = function(){
      bool <- grepl("^[ ]+",thesaurus)
      if (any(bool)){
        cat (sum(bool), "lignes débutant avec un espace, espace retiré \n")
        thesaurus <<- gsub("^[ ]+","",thesaurus)
      } else {
        cat ("aucune ligne débutant avec un espace \n")
      }
    },

    retirer_accent = function(){
      thesaurus <<- iconv(thesaurus, to="ASCII//TRANSLIT")
      cat ("Tous les accents ont été retirés \n")
    },



    set_lignes_entrees = function (){
      ######### je repère les entrées (molécule ou famille)
      ## ça commence par 2 majuscules
      regex_entrees <- "^[A-Z]{2,}"

      ### regex exclus définit lors de l'initialization
      bool_exclus <- grepl(regex_exclus, thesaurus)
      bool_inclus <- grepl (regex_entrees, thesaurus)
      bool_entrees <- bool_inclus & !bool_exclus
      lignes_entrees <<- which(bool_entrees)
      cat (length(lignes_entrees), " entrées détectées \n")
    },

    ## Vérifie si aucune entrée n'est oublié en utilisant uniquement le thésaurus
    verif_entrees = function(){
      regex_interaction <- "^[+]"
      regex_miniscules <- "[a-z]+"
      bool_lignes_vides <- thesaurus == ""
      bool_lignes_entrees <- c(1:length(thesaurus)) %in% lignes_entrees
      bool_lignes_exclus <- grepl(regex_exclus, thesaurus)
      cat ("on enlève toutes les lignes avec une entrée, une interaction (+) ou une description (minuscules) \n")
      ## j'enlève toutes les lignes concernant une entrées, une interaction, une description (miniscule), les lignes vides
      bool <- grepl(regex_interaction,thesaurus) |  grepl(regex_miniscules,thesaurus) |  bool_lignes_vides | bool_lignes_entrees | bool_lignes_exclus
      if (length(thesaurus[!bool]) != 0){
        print ("Des nouvelles lignes sont inconnus : ")
        print (thesaurus[!bool])
      } else {
        print ("Aucune autre lignes avec du contenu détecté par élimination")
      }
    },

    ### Vérifie si aucune entrée n'est oublié en utilisant les autres documents
    verif_entrees2 = function(){

    if (is.null(molecules_seules) | is.null(mol_famille)){
      stop("molecules_seules ou mol_famille non chargés")
    }
    cat ("Vérification que les ", length(lignes_entrees), " entrées du thésaurus sont connus des fichiers annexes \n")
    entrees <- thesaurus[lignes_entrees]
    bool <- entrees %in% mol_famille$molecule | entrees %in% mol_famille$famille | entrees %in% molecules_seules$molecule
    print (paste ("entrée du thésaurus inconnue des autres fichiers : ", entrees[!bool]))

    #### les préservatifs n'ont pas de RCP / code CIS

    #### vérif : toutes les familles sont présentes en entrées dans le thésaurus :
    cat ("Vérification que les ", length(mol_famille$famille), " familles de mol_famille sont présents en entrées dans le thésaurus \n")
    bool <- mol_famille$famille %in% entrees
    print (paste (
      "Famille du fichier classe thérapeutique non présente dans le thésaurus : ",
      paste (unique(mol_famille$famille[!bool]), collapse=" ; ")))

    cat ("Vérification que les ", length(molecules_seules$molecule), " molécules seules de molecules_seules sont présents en entrées dans le thésaurus \n")
    #### vérif : toutes les molécules seules sont en entrées
    bool <- molecules_seules$molecule %in% entrees
    print (paste (
      "Molécules du fichier molécule seule non présente dans le thésaurus : ",
      paste (unique(molecules_seules$molecule[!bool]), collapse=" ; ")))
    },

    remove_entrees = function (nom_entree){
      ligne <- which(thesaurus == nom_entree)
      bool <- ligne %in% lignes_entrees
      bool2 <- lignes_entrees %in% ligne
      if (any(bool)){
        cat (nom_entree, "détecté et retiré \n")
        lignes_entrees <<- lignes_entrees[!bool2]
      } else {
        cat (nom_entree, "non détecté")
      }
    },


    thesaurus_to_df = function(){
      #     lignes_entrees <- test$lignes_entrees
      #     thesaurus <- test$thesaurus
      ### fonctions permettant de splitter sur un index :
      splitAt <- function(x, pos) {
        unname(split(x, cumsum(seq_along(x) %in% pos)))}

      df2 <- NULL
      for (i in 1:(length(lignes_entrees))){
        ### pour faire la dernière ligne :
        if (lignes_entrees[i] == max (lignes_entrees)){
          des_interaction <- thesaurus[lignes_entrees[i]:length(thesaurus)]
        } else {
          ### plusieurs intéractions pour un médocs :
          des_interaction <- thesaurus[lignes_entrees[i]:(lignes_entrees[i+1]-1)]
        }
        entree <- des_interaction[1]
        ## découpage de l'interaction
        regex_int <- ("^\\+ (.*)+$")
        une_interaction <- str_extract (des_interaction,regex_int)
        bool <- !is.na(une_interaction)
        lignes_interaction <- which(bool)
        noms_interaction <- une_interaction[lignes_interaction]
        noms_interaction <- gsub ("^\\+ ","",noms_interaction)

        liste_interaction <- splitAt(des_interaction, lignes_interaction)

        description <- lapply(liste_interaction, function(x){
          bool <- x == ""
          x[bool] <- "\n"
          x <- paste (x[2:length(x)], collapse=" ")
          x <- gsub("^\n|\n$","",x)
        })

        #### on enlève le premier qui est le nom du médoc mais parfois donne des informations supplémentaires : voir aussi, liste des médocs
        description_medoc <- liste_interaction[1]
        description_medoc <- unlist(description_medoc)[-1]
        description_medoc <- paste (description_medoc, collapse="")

        description <- description[-1]
        description <- unlist(description)

        test <- data.frame (entree = entree, interaction = noms_interaction, description_interaction = description, description_medoc = description_medoc)
        df2 <- rbind (df2, test)
      }
      df <<- df2
      df$interaction <<- gsub ("^[ ]+|[ ]+$","",df$interaction)
      df$interaction <<- as.character(df$interaction)
      df$description_medoc <<- gsub  ("\\(voir aussi \"bradycardisants\"\\)","Voir aussi : bradycardisants", df$description_medoc)
      df$entree <<- gsub ("^[ ]+|[ ]+$","",df$entree)
      cat ("thésaurus transformé en dataframe : df \n")
    },

    retire_AUTRES = function(){
      cat ("Ces interactions commençant par AUTRES ... signifient
      qu'il ne faut pas associer 2 molécules d'une même famille, on retire AUTRES \n")
      bool <- grepl("^AUTRES ",df$interaction) & !grepl("CORTICOIDES",df$interaction)
      df$interaction[bool] <<- gsub ("^AUTRES ", "", df$interaction[bool])
      cat (sum(bool), " noms de protagonistes commençant par AUTRES modifiés \n")
    },

    retire_MEDICAMENTS = function(){
      #### il y a des familles à traiter manuellement
      cat ("on réécrit les noms de certaines familles commenaçant par 'MEDICAMENTS' et FIBRATES (AUTRES) \n")
      df$interaction <<- gsub ("MEDICAMENTS ANTICHOLINESTERASIQUES", "ANTICHOLINESTERASIQUES", df$interaction)
      df$interaction <<- gsub ("MEDICAMENTS HYPONATREMIANTS", "HYPONATREMIANTS", df$interaction)
      df$interaction <<- gsub ("FIBRATES \\(AUTRES\\)", "FIBRATES", df$interaction)
    },

    ### Vérifie si aucune interaction n'est inconnu en utilisant les autres documents
    verif_interaction = function(){
      if (is.null(molecules_seules) | is.null(mol_famille)){
        stop("molecules_seules ou mol_famille non chargés")
      }
      cat ("Vérification que les ", nrow(df$interaction), " interactions (+) du thésaurus sont connus des fichiers annexes \n")
      bool <- df$interaction %in% mol_famille$famille | df$interaction %in% mol_famille$molecule |
        df$interaction %in% molecules_seules$molecule
      interaction_inconnu <- unique(as.character(df$interaction[!bool]))
      interaction_inconnu <- paste ("\t", interaction_inconnu)
      interaction_inconnu <- paste (interaction_inconnu, collapse="\n")
      cat (paste ("Interactions inconnues : \n ",interaction_inconnu))
    },

    ### Molécules restantes :
    # cat("Ces interactions n'ont pas de molécules ou médicaments associées.
    # On peut ignorer les aliments (mettre une information),
    # pour les médicaments par voie orale et par voie vaginale, on se sert de la voie
    # d'administration pour les constitutés ;
    # Pour les médicaments agissant sur l'hémostase : à constituer soit meme
    # De meme pour les sels de fer par voie injectable")

    add_mecanisme_explication = function(){
      ######## Séparer le mécanisme quand ça contient \n
      df$description_interaction <<- gsub ("^[ ]+|[ ]+$","",df$description_interaction)
      ### si ça contient \n c'est potentiellement un mécanisme
      bool <- grepl("\n(.)*",df$description_interaction)
      temp <- str_extract_all(df$description_interaction,"\n(.)*")
      temp <- lapply(temp, function(x){
        x <- paste (x, collapse="")
      })
      temp <- unlist(temp)
      df$mecanisme <<- temp

      ## si c'est collé, c'est un mécanisme
      bool <- grepl("^(Association DECONSEILLEE|CONTRE-INDICATION|A prendre en compte|Precaution d'emploi)[A-Za-z]",df$description_interaction)
      df$gauche <<- ifelse (bool,1,0)
      ## on overwrite le mecanisme
      df$mecanisme[bool] <<- df$description_interaction[bool]
      df$mecanisme <<- gsub("\n","",df$mecanisme)
      df$mecanisme <<- gsub ("^[ ]+|[ ]+$","",df$mecanisme)
      df$mecanisme <<- gsub ("[ ]+"," ",df$mecanisme)
      ## Enlever les précautions d'emploi ...
      df$mecanisme <<- gsub ("(Association DECONSEILLEE|CONTRE-INDICATION|A prendre en compte|Precaution d'emploi)","",df$mecanisme)

      ## on retire de la description tout ce qui suit un saut de ligne (le mécanisme)
      df$description_interaction <<- gsub("\n(.)*","",df$description_interaction)
      ## quand on retire le niveau, la description devient l'explication
      df$explication <<- gsub ("(Association DECONSEILLEE|CONTRE-INDICATION|A prendre en compte|Precaution d'emploi)","",df$description_interaction)
      df$explication <<- gsub ("[ ]+"," ",df$explication)
      ## si c'est collé, il n'y a pas d'explication
      df$explication <<- ifelse (df$gauche == 1, "",df$explication)
      df$description_interaction <<- gsub ("^Association DECONSEILLEE","Association DECONSEILLEE ",df$description_interaction)
      df$description_interaction <<- gsub ("^CONTRE-INDICATION","CONTRE-INDICATION ",df$description_interaction)
      df$description_interaction <<- gsub ("^A prendre en compte","A prendre en compte ",df$description_interaction)
      df$description_interaction <<- gsub ("[ ]+"," ",df$description_interaction)
      df$gauche <<- NULL
    },



    ## dans la description des entrées (df$description_medoc), il y a la liste des molécules
    # on vérifie si ça correspond bien avec les documents de mol_famille
    verif_mol_famille = function(){
      if (is.null(molecules_seules) | is.null(mol_famille)){
        stop("molecules_seules ou mol_famille non chargés")
      }
      ### VOIR AUSSI - famille de la molécule en entrées
       regex_voir_aussi <- "^Voir aussi : "
       bool <-  grepl(regex_voir_aussi, df$description_medoc)
      #df$description_medoc[bool]
      ##### les médicaments en entrées ont une interaction propre et orientés vers les familles pour les autres interactions

      check <- subset (df, bool, select=c("entree","description_medoc"))
      colnames(check) <- c("entites","famille")
      check$entites <- as.character(check$entites)
      check$famille <- gsub ("^Voir aussi : ", "", check$famille)
      check <- unique(check)

      nombres_rep <- unlist(lapply (str_split(check$famille," - "), length))
      nom_entite <- c()
      for (i in 1:length(nombres_rep)){
        nom_entite <- append (nom_entite, rep(check$entites[i], nombres_rep[i]))
      }
      nom_medocs <- unlist(str_split(check$famille," - "))
      if (length(nom_medocs) == length(nom_entite)){
        df_explose <- data.frame (entites=nom_entite, medocs=nom_medocs)
        df_explose$medocs <- gsub ("^ ","",df_explose$medocs)
      } else {
        stop ("Probleme pour exploser les médocs")
      }
      df_explose$medocs <- toupper(df_explose$medocs)
      temp1 <- paste (df_explose$entites, df_explose$medocs,sep=";")
      temp2 <- paste (mol_famille$molecule, mol_famille$famille,sep=";")
      temp2 <- toupper(temp2)
      bool <- temp1 %in% temp2
      absents <- paste (paste ("\t", temp1[!bool]), collapse="\n")
      cat ("Couples présents dans le thésaurus et non retrouvés dans le pdf
    classe thérapeutique : \n", absents)
    },

    ## si c'est une famille en entrée => on a une liste de médocs
    ## si c'est une molécule => on a Voir aussi : la famille
    # sauf pour un cas : les anticholinestérases où on a voir aussi les bradycardisants
    ## donc on vérifie que les molécules sont bien dans la même famille
    ## et les familles ont toutes leurs molécules
    verif_famille_entrees = function(){
    regex_voir_aussi <- "^Voir aussi : "
    bool <-  grepl(regex_voir_aussi, df$description_medoc)
    description_medoc2 <- ifelse (bool, NA, as.character(df$description_medoc))
    description_medoc2 <- ifelse (description_medoc2 == "", NA, as.character(description_medoc2))

    regex_liste_molecule <- "\\.\\((.*)+"
    ##### les molécules peuvent être après du blabla
    bool <- grepl("^\\(", description_medoc2) | grepl (regex_liste_molecule, description_medoc2)
    #description_medoc2[bool]
    check <- data.frame(entree = df$entree,description_medoc2=description_medoc2)
    check <- unique(check)
    ######## j'enlève le blabla pour certains :
    bool <- grepl (regex_liste_molecule, check$description_medoc2)
    check$description_medoc2 <- ifelse (bool, str_extract(check$description_medoc2,regex_liste_molecule), check$description_medoc2)
    check$description_medoc2 <- gsub("^\\.","",check$description_medoc2)

    colnames(check) <- c("entites","famille")
    check$entites <- as.character(check$entites)
    check$famille <- gsub ("^\\(","",check$famille)
    check$famille <- gsub ("\\)$","",check$famille)
    nombres_rep <- unlist(lapply (str_split(check$famille,","), length))
    nom_entite <- c()
    for (i in 1:length(nombres_rep)){
      nom_entite <- append (nom_entite, rep(check$entites[i], nombres_rep[i]))
    }
    nom_medocs <- unlist(str_split(check$famille,","))
    if (length(nom_medocs) == length(nom_entite)){
      df_explose <- data.frame (entites=nom_entite, medocs=nom_medocs)
      df_explose$medocs <- gsub ("^ ","",df_explose$medocs)
    } else {
      stop ("Probleme pour exploser les médocs")
    }
    colnames(df_explose) <- c("famille","molecule")
    df_explose$molecule <- toupper(df_explose$molecule)
    voir <- subset (mol_famille, famille %in% df_explose$famille)
    bool <- df_explose$molecule %in% mol_famille$molecule
    #### quelle famille n'est pas présente en entrée dans le thésaurus ?
    bool <- mol_famille$famille %in% df_explose$famille
    print ("Famille en entrée qui ne décrit pas ses molécules :")
    print (unique(mol_famille$famille[!bool]))
    },

    #### dans la description de l'entrée, il y a parfois plus de texte :
    contenu_description_hors_molecules = function(){
      regex_voir_aussi <- "^Voir aussi : "
      bool <-  grepl(regex_voir_aussi, df$description_medoc)
      description_medoc2 <- ifelse (bool, NA, as.character(df$description_medoc))
      description_medoc2 <- ifelse (description_medoc2 == "", NA, as.character(description_medoc2))
      bool <- grepl("^\\(", description_medoc2)
      description_medoc2 <- ifelse (bool, NA, description_medoc2)
      regex_liste_molecule <- "\\.\\((.*)+"
      description_medoc2 <- gsub (regex_liste_molecule, "",description_medoc2)
      bool <- !is.na(description_medoc2)
      voir <- subset (df, bool)
      temp <- unique(voir$description_medoc2)
      temp <- as.character(temp)
      length(temp)
      print(temp)
    },

    #### un commentaire est inhabituel, il est remplacé manuellement :
    replace_il_convient = function(){
      bool <- grepl ("^Il convient de prendre en compte", df$description_interaction)
      if (any(bool)){
        cat ("^Il convient de prendre en compte remplacé par A prendre en compte : ",sum(bool), "\n")
        df$description_interaction[bool] <<- gsub ("^Il convient de prendre en compte",
                                                       "A prendre en compte Il convient de prendre en compte",
                                                       df$description_interaction[bool])
        } else {
        cat ("^Il convient de prendre en compte : non détecté \n")
      }
    },

    ### Le niveau est décrit dans la description de l'interaction
    ## l'objectif ici est de mettre le coutenu de cette description dans l'une des 4 colonnes : CI, AD, PE, PC
    classifie_niveau = function(){
      df$CI <<- NA
      df$AD <<- NA
      df$PE <<- NA
      df$PC <<- NA

      categorie <- c("^Precaution d'emploi","^Association DECONSEILLEE","^A prendre en compte"
                     ,"^CONTRE-INDICATION", "^CI","ASDEC","APEC"," PE ")
      colonnes <- c("PE","AD","PC","CI","CI","AD","PC","PE")

      df_regex_colonne <- data.frame (regex = categorie,colonne = colonnes, stringsAsFactors = F)
      df$description_interaction <<- gsub("^\n ", "",df$description_interaction)
      bool <- c("regex","colonne")  %in%  colnames(df_regex_colonne)
      if (!all(bool)){
        stop ("pas les bonnes colonnes dans la table df_regex_colonne")
      }

      bool <- c("explication","description_interaction","CI","AD","PE","PC") %in% colnames(df)
      if (!all(bool)){
        stop ("pas les bonnes colonnes dans la table df")
      }

      i <- 8
      for (i in 1:nrow(df_regex_colonne)){
        bool <- grepl (df_regex_colonne$regex[i],df$description_interaction)
        if (!any(bool)){
          print (df_regex_colonne$regex[i])
          stop("Erreur, aucune description d'interaction trouvée avec ce regex")
        }
        colonne_choisi <- colnames(df) %in% df_regex_colonne$colonne[i]
        ## je mets l'explication plutôt que la description qui contient aussi le mécanisme
        df[,colonne_choisi][bool] <<- df$explication[bool]
      }
      df$explication <<- NULL
      cat ("4 colonnes créés dans la df : CI, AD, PC, PE")
    },

    verif_absence_de_niveau = function(){
      bool <- is.na(df$CI) & is.na(df$PC) & is.na(df$PE) & is.na(df$AD)
      if (any(bool)){
        cat (sum(bool), "lignes n'ont pas de niveau \n")
        voir <- subset (df, bool)
        return(voir)
      } else {
        cat ("Toutes les lignes de la df ont un niveau \n")
      }
    },

    df_sans_doublon = function(){
      temp <- paste (df$entree, df$interaction, sep=";")
      temp <- lapply (temp, function(x){
        test <- unlist(str_split(x,";"))
        test <- sort (test)
        test <- paste (test, collapse=";")
      })
      temp <- unlist(temp)
      df$couple <<- temp
      ###
      tab <- table(temp)
      tab <- data.frame (couple = names(tab), frequence = as.numeric(tab))

#       ##
#       tab_temp1 <- subset (tab, frequence == 2)
#       df2 <- subset (df, couple %in% tab_temp1$couple)
#       nrow(df2) / 2
#       ##

      cat (sum(tab$frequence == 2), "couples A-B en double : (A-B) puis (B-A) \n")
      cat ("la data.frame va donc passer de ", nrow(df), "à ", nrow(df) - sum(tab$frequence == 2), "lignes\n")
      bool <- df$entree == df$interaction
      cat (sum(bool), "couples A-A \n")
      cat (nrow(df) - sum(tab$frequence == 2)*2 - sum(bool), "couples A-B n'apparaissent pas en double \n")

      ### on enlève tous les doublons
      df$temp <<- 1:nrow(df)
      tab <- tapply(df$temp, df$couple, min)
      tab <- data.frame (couple = names(tab), temp = as.numeric(tab))

#       ### insert ici le check_miroir :
#       df2$temp <- 1:nrow(df2)
#       tab <- tapply(df2$temp, df2$couple, min)
#       tab <- data.frame (couple = names(tab), temp = as.numeric(tab))
#       tab2 <- tapply(df2$temp, df2$couple, max)
#       tab2 <- data.frame (couple = names(tab2), temp = as.numeric(tab2))
#       df2_tab <- merge (df2, tab, by=c("couple","temp"))
#       df2_tab2 <- merge (df2, tab2, by=c("couple","temp"))
#       df2_tab$temp <- NULL
#       df2_tab2$temp <- NULL
#       df3 <- merge (df2_tab, df2_tab2, by="couple")
#       colnames(df3)
#       bool <- df3$PE.x == df3$PE.x
#       bool <- is.na(df3$AD.x) & is.na(df3$AD.y) | df3$AD.x == df3$AD.y
#       all(bool)
#       all(bool,na.rm = T)
#       voir <- subset (df3, !bool)
#       voir <- subset (df3, is.na(bool))
#       voir$PC.x[1]
#       voir$description_interaction.y[1]
#       ###

      df <<- merge (df, tab, by=c("couple","temp"))
      df$couple <<- NULL
      df$temp <<- NULL
    },

      set_df_decompose = function(){
        df2 <- df
        df2$niveau <- ifelse (!is.na(df$PC), 1,
                              ifelse (!is.na(df$PE), 2,
                                      ifelse (!is.na(df$AD), 3,
                                              4)))
        ## niveau par protagoniste
        colnames(df2)[1:2] <- c("prota1","prota2")
        ######## remplacer les familles par leurs molécules
        ### remplacer prota1 par sa liste de molécules
        tab1 <- merge (df2, mol_famille, by.x="prota1",by.y="famille",all.x = T)
        ## si la jointure est NA alors prota1 est une molécule
        colnames(tab1)[length(tab1)] <- c("mol1")
        tab1$mol1 <- ifelse (is.na(tab1$mol1), tab1$prota1, tab1$mol1)
        ### remplacer prota2
        tab2 <- merge (tab1, mol_famille, by.x="prota2",by.y="famille",all.x = T)
        colnames(tab2)[length(tab2)] <- c("mol2")
        tab2$mol2 <- ifelse (is.na(tab2$mol2), tab2$prota2, tab2$mol2)
        ### le problème est qu'une interaction entre 2 molécules peut avoir plusieurs origines
        ##  doublons : molécule1- molécule2 et molécule2-molécule1
        ## et aussi plusieurs niveaux
        
        ## couple de 2 molécules
        tab2$both <- paste(tab2$mol1, tab2$mol2, sep=";")
        temp <- lapply(tab2$both, function(x){
          essai <- unlist(strsplit(x,";"))
          essai <- sort(essai)
          essai <- paste(essai,collapse=";")
        })
        temp <- as.character(unlist(temp))
        # couple par ordre alphabétique
        tab2$both2 <- temp
        
        ### reordonne les molécules
        tab2$mol1 <- sapply(tab2$both2, function(x){
          unlist(strsplit(x,";"))[1]
        })
        tab2$mol2 <- sapply(tab2$both2, function(x){
          unlist(strsplit(x,";"))[2]
        })
        tab2$both <- NULL
        tab2$both2 <- NULL
        df_decompose <<- tab2
      },

      check_decompose=function(){
        mol_decompose <-unique (c(df_decompose$mol1, df_decompose$mol2))
        bool <- mol_decompose %in% mol

        cat("mol1 ou mol2 de df_decompose non listées dans les fichiers index : ")
        print (mol_decompose[!bool])

        bool <- mol %in% mol_decompose
        if (any(bool)){
          cat("molécules dans fichiers index non présentes dans df_decompose : ")
          print (mol[!bool])
        }
      },

    create_manuellement = function(){
      nombres_niveaux <- data.frame (CI =as.numeric(is.na(df$CI)), PC= as.numeric(is.na(df$PC))
                                     , PE = as.numeric(is.na(df$PE)), AD= as.numeric(is.na(df$AD)))
      nombre_niveaux <- rowSums(nombres_niveaux)
      nombre_niveaux <- 4 - nombre_niveaux
      manuellement <<- subset (df, nombre_niveaux  > 1)
      cat (nrow(manuellement), "lignes ont plusieurs niveaux d'interaction \n")
    },

    load_manuellement = function(fichier_manuellement){
      manuellement_fait <- read.table(fichier_manuellement,sep="\t",quote="",header=T)
      if (length(setdiff(colnames(manuellement), colnames(manuellement_fait))) != 0){
        stop("Les data.frames n'ont pas les mêmes colonnes")
      }
      manuellement <<- manuellement_fait
      cat ("la df manuellement a été remplacé par le fichier ", fichier_manuellement, " \n")
      cat ("Charger ce fichier dans df avec 'replace_manuellement' \n")
    },

    replace_manuellement = function(){
      both_manu <- paste (manuellement$entree, manuellement$interaction, sep=";")
      both_df <- paste (df$entree, df$interaction, sep=";")
      df <<- subset (df, !both_df %in% both_manu)
      df <<- rbind (df, manuellement)
      cat ("manuellement a été ajouté à df \n")
    },

pb_2009_famille_heparine = function(){
  bool <- thesaurus == "AGE)"
  bool2 <- grepl("+ HEPARINES DE BAS POIDS MOLECULAIRE ET APPARENTES (DOSES CURATIVES ET/OU SUJET ",thesaurus,fixed = T)
  if (any(bool | bool2)){
    cat ("problème avec la famille des topiques grastro intestinaux détecté ...  ")
    thesaurus[bool] <<- ""
    thesaurus[bool2] <<- gsub ("+ HEPARINES DE BAS POIDS MOLECULAIRE ET APPARENTES (DOSES CURATIVES ET/OU SUJET",
                              "+ HEPARINES DE BAS POIDS MOLECULAIRE ET APPARENTES (DOSES CURATIVES ET/OU SUJET AGE)",
                              thesaurus[bool2],fixed = T)
    cat ("problème résolu \n")
  } else {
    cat ("aucun problème HEPARINES DE BAS POIDS MOLECULAIRE détecté \n")
  }
},
pb_2016_famille_absorbant = function(){
      bool <- thesaurus == "ADSORBANTS"
      bool2 <- grepl("SUBSTANCES A ABSORPTION REDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET",thesaurus)
      if (any(bool | bool2)){
        cat ("problème avec la famille des topiques grastro intestinaux détecté ...  ")
        thesaurus[bool] <<- ""
        thesaurus[bool2] <<- gsub ("SUBSTANCES A ABSORPTION REDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET ",
                                  "SUBSTANCES A ABSORPTION REDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET ADSORBANTS", thesaurus[bool2])
        bool <- thesaurus == "ADSORBANTS"
        bool2 <- grepl("SUBSTANCES A ABSORPTION REDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET",thesaurus)
        cat ("problème résolu \n")
      } else {
        cat ("aucun problème avec la famille des topiques grastro intestinaux détecté \n")
      }
    },
    pb_2015_faute_racecadodril = function(){
      bool <- molecules_seules$molecule == "RACECADODRIL"
      if (any(bool)){
        molecules_seules$molecule[bool] <<- "RACECADOTRIL"
        cat ("Faute d'orthographe de RACECADOTRIL corrigé dans molécules_seules \n")
      } else {
        cat ("Pas de faute d'orthographe de RACECADOTRIL détectée \n")
      }
    }
  )
)
