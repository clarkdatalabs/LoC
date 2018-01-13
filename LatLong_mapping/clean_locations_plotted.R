if (!require("pacman")) install.packages("pacman")
pacman::p_load('dplyr', 'tidyverse', RSQLite)


data <- read.csv("Location_joined.csv", stringsAsFactors = FALSE)

get_country <- function(a,b) ifelse(grepl('^[A-Za-z]+$', a), a, b)




data <- data %>%
  mutate(country = get_country(ISO_A2, ISOalpha2)) %>% 
  transmute(locationString = locationSt
            , latitude = latitude
            , longitude = longitude
            , ISOalpha2 = country
            , USAstate = USAstate)
 
write.csv(data
          , file = "Location_joined_cleaned.csv"
          , row.names = FALSE)
