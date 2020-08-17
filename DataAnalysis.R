library(smooth)
library(zoo)
library(dplyr)

data <- read.csv("dataAll.csv")
data$date <- as.Date(data$date)

per <- 30
av = rollmean(data$score,per)

plot(data$date[per:length(data$date)],av,ylim=c(-0.3,0.3),type="l", main="/r/All")
abline(h=0.05, col="red")
abline(h=-0.05, col="red")
abline(v=17186, col = "blue")



getdate <- function(){
  date = round(locator()[1]$x)
  for (i in 1:length(date)){
    print(tweets$date[tweets$date==date[i]])
  }
}


tweets <- read.csv("tweetScore.csv")
tweets$date <- as.Date(tweets$created_at)
tweets <- tweets %>% group_by(date) %>% summarise(Mscore=mean(score))

plot(tweets$date,tweets$Mscore)


