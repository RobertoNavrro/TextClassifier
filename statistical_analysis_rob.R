library(ggplot2)
library(car)

results <- read.table("D:/Documents/University/UU/MAIR/Projects/TextClassifier/data/questionnaire_answers.csv",
                      header = TRUE, sep = ",")

to_change = c("too_complex", "need_support", "too_inconsistent", "cumbersome", "need_learn")
for (column in to_change) {
  x = results[, column] - 3
  results[, column] = rep(3, length(x)) - x
}


results$sum = rowSums(results[,!names(results) %in% c("Tijdstempel", "participant_number", "group")])
results$sum = results$sum * 2
results$group = as.factor(results$group)

group1 = c(46,96,80,72,76,82,78,78,52,72,52,82)
group2 = c(66,74,78,76,36,76,40,84,68,82,90,82)

median(group1)
median(group2)

#Check Homogeniety of variance assumption: passes!
leveneTest(sum ~ group, data=results)

qqnorm(results$sum)
qqline(results$sum, col= "steelblue", lwd = 2)

#Check normality assumption: Does not pass!
shapiro.test(results$sum)-


#t.test(sum ~ group, data=results)

wilcox.test(sum ~ group, data=results, correct=FALSE, exact= FALSE, conf.int = TRUE)

plot <- ggplot(results, aes(group, sum)) + geom_boxplot() + xlab("Group") + ylab("System Usability Score")
plot = plot  + ggtitle("Results SUS by group") + theme(plot.title = element_text(hjust = 0.5))
plot

