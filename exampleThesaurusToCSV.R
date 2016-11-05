library(IMthesaurusANSM)
## list of extracted thesaurus :
d <- data(package = "IMthesaurusANSM")
d$results[,"Item"]

## load a thesaurus, ex : thesaurus82016
thesaurus <- thesaurus82016
class(thesaurus) ## an object of class Thesaurus
## list of the fields :
?Thesaurus

## thesaurus after extraction 
df <- thesaurus$df
colnames(df)[1:2] <- c("protagoniste1","protagoniste2")
write.table(df, "CSVfiles/thesaurusAout2016.csv",sep="\t",col.names=T, row.names=F, quote=F)

## replacing all the therapeutic classes by their drug substances
df <- thesaurus$df_decompose
df <- unique(df)
#write.table(df, "CSVfiles/thesaurusAout2016Decompose.csv",sep="\t",col.names=T, row.names=F, quote=F)

## list of drugs substances - therapeutic class : 
df <- thesaurus$mol_famille
write.table(df, "CSVfiles/moleculesfamillesAout2016.csv",sep="\t",col.names=T, row.names=F, quote=F)

## list of drugs : 
drugs <- thesaurus$mol
length(drugs)
writeLines(drugs, "CSVfiles/moleculesAout2016.txt")
