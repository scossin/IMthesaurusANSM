### création d'un script pour lancer tous les fichiers en shell
# fichier à lancer
fichiers <- list.files(recursive = T,full.names = T)
bool <- grepl("thesaurus",fichiers) & grepl(".R$", fichiers) & 
  grepl("[0-9]+/R/", fichiers)
fichiers <- fichiers[bool]


## besoin de changer cd à chaque fois
library(stringr)
nomfichier <- stringr::str_extract(fichiers,"[a-z0-9.R]+$")
nomrepertoire <- fichiers
for (i in nomfichier){
  nomrepertoire <- gsub (i, "",nomrepertoire)
}

# commande : 
commande <- paste ("Rscript ",nomfichier,sep="")

output <- NULL
for (i in 1:length(commande)){
  output <- append (output, paste ("cd ", nomrepertoire[i],sep=""))
  output <- append (output, commande[i])
  output <- append (output, "cd ../../")
}
# output
writeLines(output,"update.sh")
