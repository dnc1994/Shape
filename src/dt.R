library(caret)
library(rpart)
library(ggplot2)

setwd("C:/Home/Projects/Shape/data/train_feature")

data <- read.csv("train_feature.csv")
summary(data)

obj_func <- formula(label ~ Thinness + Extent)
dt_model <- rpart(obj_func, method="class", data=data)
print(dt_model)
