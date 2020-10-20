library(ggplot2)

results <- read.table("C:/Users/Quintess/Documents/Uni/Master/Jaar 1/methods in AI research/project/TextClassifier/data/questionnaire_answers.csv",
                     header = TRUE, sep = ",")

to_change = c("too_complex", "need_support", "too_inconsistent", "cumbersome", "need_learn")
for (column in to_change) {
  x = results[, column] - 3
  results[, column] = rep(3, length(x)) - x
}


results$sum = rowSums(results[,!names(results) %in% c("Tijdstempel", "participant_number", "group")])
results$sum = results$sum * 2
results$group = as.factor(results$group)

t.test(sum ~ group, data=results)

plot <- ggplot(results, aes(group, sum)) + geom_boxplot() + xlab("Group") + ylab("System Usability Score")
plot = plot  + ggtitle("Results SUS by group") + theme(plot.title = element_text(hjust = 0.5))
plot
