if (!require("pacman")) install.packages("pacman")
pacman::p_load('dplyr', 'tidyverse')


setwd("C://Users/DJT/workspace/LoC")
d <- read.csv("Visualization/location_by_year.csv")


min_year <- 1050
max_year <- 2014



dSmooth <- data.frame( pubDate = seq(min_year, max_year)) %>% 
  merge(data.frame(unique(d[,c("ISOnumeric3", 
                               "countryName", 
                               "ISOalpha2", 
                               "ISOalpha3")]))) %>% 
  left_join(d) %>% 
  mutate(count = ifelse(is.na(count), 0, count)) %>% 
  mutate(smooth.3 = 0,
         smooth.5 = 0)

#unique(d$ISOnumeric3)

test <- dSmooth %>% 
  filter(ISOnumeric3 == 894) %>% 
  arrange(pubDate)

year <- 1988
t3 <- mean(test[test$pubDate %in% (year-2):year,c("count")])
t5 <- mean(test[test$pubDate %in% (year-4):year,c("count")])
test[(test$ISOnumeric3 == 894) & (test$pubDate == year),
        c("smooth.3", "smooth.5")] <- c(t3,t5)


for (country in unique(d$ISOnumeric3)){
  dCountry <- dSmooth %>% 
    filter(ISOnumeric3 == country) %>% 
    arrange(pubDate)
  for (year in (min_year+9):max_year){
    m3 <- mean(dCountry[dCountry$pubDate %in% (year-2):year,c("count")])
    m5 <- mean(dCountry[dCountry$pubDate %in% (year-4):year,c("count")])
    dSmooth[(dSmooth$ISOnumeric3 == country) & (dSmooth$pubDate == year),
            c("smooth.3", "smooth.5")] <- c(m3,m5)

    
  }
}

write.csv(dSmooth, "smooth_data/location_by_year_smooth_(FULL).csv")





###READ IN ABOVE TABLE, DROP ROWS

dSmooth <- read.csv("smooth_data/location_by_year_smooth_(FULL).csv")

dSmooth.clean <- dSmooth[!(dSmooth$smooth.5 == 0),]
dSmooth.clean$smooth.3 <- (dSmooth.clean$smooth.3*3)
dSmooth.clean$smooth.5 <- (dSmooth.clean$smooth.5*5)
dSmooth.clean <- rename(dSmooth.clean, smooth3 = smooth.3, smooth5 = smooth.5)

write.csv(dSmooth.clean, "smooth_data/location_by_year_smooth.csv")

