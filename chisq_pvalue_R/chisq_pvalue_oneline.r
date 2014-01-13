argss <- commandArgs(trailingOnly=TRUE)

pos1 <- as.numeric(argss[2])
pos2 <- as.numeric(argss[3])
pos3 <- as.numeric(argss[4])
pos4 <- as.numeric(argss[5])

rr=chisq.test(rbind(c(pos1,pos2),c(pos3,pos4)))
cat(sprintf("%s\t%s\n", rr[1], rr[3]))
