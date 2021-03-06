## Xaltius TravelTomo

# Purpose
This script demonstrates data collection techniques
The information gathered from TripAdvisor.com and stored
in a pandas dataframe or directly to an SQL server

## tripAdvisor.py
This code takes data from Trip Advisor about attractions in the location/city, to be
to be cleaned using pandas, and analyzed with machine learning. 

## Data Gathered
The fields of the dataframe which were collected for each "thing to do"

### Title
 The title of each attraction, resuturant, or location
### Rating
 A decimal score up to 5.0
### Review Count
 The total number of user reviews
### Phone Number
 The phone number and country code
### Address
 The street address, if it exists
### Locality
 The locality (usually zip code and province)
### Date Generated
 The date the list was generated as a datetime object
### Keywords
 Most common tags/keywords used in the user review section, stored as dictionary with
 each keyword as the key and the frequency of its occurance as the value
### Estimated Duration of Visit
 The estimated duration to spend at each location given by Trip Advisor, if it exists
### Estimated Cost
 The estimated cost in the displayed local currency
### User Review Table
 Contains user reviews, usernames, ratings, dates, and user locations

## genCountryTable.py
This used a wikipedia article on ISO 3166-1 alpha-2 to scrape a table of 2 letter country codes from the ISO 3166 standard. Used to fill the country table

### Country Table
 Contains info such as population, GDP, currency, pop. density, demographics