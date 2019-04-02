# Adapted from http://www.sthda.com/english/wiki/kruskal-wallis-test-in-r

# Read in your .csv file and assign to variable.
my_data <- read.csv(file.choose())


head(my_data)

levels(my_data$Group)

#If you want to change the order of your experimental groups perform the "ordered" function
#and list out the order you want
my_data$Group <- ordered(my_data$Group,
                         levels = c("lacZ -ATR -TTX", "lacZ +ATR -TTX", "lacZ -ATR +TTX", "lacZ +ATR +TTX", "Unc5 -ATR -TTX", "Unc5 +ATR -TTX", "Unc5 -ATR +TTX", "Unc5 +ATR +TTX"))

#Compute the summary statistics for each experimental group
library(dplyr)
group_by(my_data, Group) %>%
  summarise(
    count = n(),
    mean = mean(Baseline.F, na.rm = TRUE),
    sd = sd(Baseline.F, na.rm = TRUE),
    median = median(Baseline.F, na.rm = TRUE),
    IQR = IQR(Baseline.F, na.rm = TRUE)
  )

#Graph your data using box and whisker plots
library("ggpubr")
ggboxplot(my_data, x = "Group", y = "Baseline.F", 
          color = "Group", 
          order = c("lacZ -ATR -TTX", "lacZ +ATR -TTX", "lacZ -ATR +TTX", "lacZ +ATR +TTX", "Unc5 -ATR -TTX", "Unc5 +ATR -TTX", "Unc5 -ATR +TTX", "Unc5 +ATR +TTX"),
          ylab = "Baseline F (AU)", xlab = "Experimental Group")

# Mean plots
# Plot Basline.F by group
# Add error bars: mean_sd
# (other values include: mean_sd, mean_ci, median_iqr, ....)

library("ggpubr")
ggline(my_data, x = "Group", y = "Baseline.F", 
       add = c("mean_sd", "jitter"), 
       order = c("lacZ -ATR -TTX", "lacZ +ATR -TTX", "lacZ -ATR +TTX", "lacZ +ATR +TTX", "Unc5 -ATR -TTX", "Unc5 +ATR -TTX", "Unc5 -ATR +TTX", "Unc5 +ATR +TTX"),
       #color = "Group", 
       ylab = "Baseline F (AU", xlab = "Experimental Group")

#We want to know if there is any significant difference between 
#the average Baseline Fluorescence between experimental conditions.
#The test can be performed using the function kruskal.test() as follows:
  
kruskal.test(Baseline.F ~ Group, data = my_data)

  
pairwise.wilcox.test(my_data$Baseline.F, my_data$Group,
                     p.adjust.method = "BH")  

