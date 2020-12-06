## Goal
Create a linear regression that will use previous Metacritic data for actors and core crew members to predict the Metacritic score for films. 

## Motivation
Prior to the pandemic beginning in spring, I was looking forward to the summer of 2020 because Christopher Nolan was finally releasing his next film. After March that anticipation faded as New York City shutdown and didn't reopened until the early summer month. The film industry took massive losses on films such as "Birds of Prey," taking in a total gross of 200 million dollars when the breakeven for the film would have been 250-300 million dollars. Birds of Prey had a sequal that was in development that has sense been shut down by Hollywood studios due to the massive loss companies suffered because of the lacking box office. I wanted to create a model that could predict the Metacritic score of a film based on the previous performance of movies. I thought to myself about how production companies and other financing bodies for films could make up for the loss that they would continue to suffer as the pandemic continued on as they were forced movies to be released only to gross far less than they would in a normal summer film season, as well as being forced into shelving films until they could have a wide release when the pandemic ended. 

## Data
My dataset was scrapped from Metacritic using Beautiful Soup. This proved to be more difficult than with practice that I had scrapping from websites that don't have restrictions on how much you can scrape, such as Wikipedia. I used CloudScraper to help scrape more and used the Requests library to use a header for the html request that I was making. I also used the sessions object to send my requests with cookies as a last effort. In the end I scraped every movie that Metacritic had in the database. From each movie I used the user score, the metascore, and all of the cast and crew information. 

I created a database for my data in Postgres with four tables: cast and crew credits, film details (runtime, release date, language), and finally the films with their metacritic score and userscore. I created my main features for analysis by using a film's release date and all of the actors in the film to create three features, prinicple cast mean previous Metascore, supporting cast mean previous Metascore, and then the mean of all the scores combined. I did the same with the crew having 4 features in the end: directors mean previous metascore, writers, producers, and then all other crew members were pooled together for an other crew members mean metascore variable. I did the same with the userscores to create the same seven features. I had films that had null values because everyone has to start somewhere so if there was a film where no actor had a previous metascore then there was no value to report. I dropped these null values. Even without the values in the table for anaylsis the Metascores of the films were still being utilized when actors would appear in their next and all following films. 

The last bit of work I had to do getting my dataset ready for analysis was creating dummy variables. I had production companies, languages, genres, mpaa ratings, and release dates. There was a total of 10,377 production companies so I decided it was best to exclude them for the time being. I made language dummies and binned together all of the languages that weren't in the 5 most used languages: English, Spanish, French, and German. For the genre categories I kept comedy and drama separate and then binned the other genres into action and adventure, suspense, and others. Lastly, I used the release month and kept the month of release and binned the months into seasons. 

## Feature Selection
I ran an inital regression of my data using StatsModels linear regression. The condition number was high and indicated that multicolinearity was having an effect on the model. The R^2 was .52 for my initial model.

For feature selection the main goal that I had was reducing mulitcolinearity and heteroskedasticity. I found the variance inflation factor for each feature to identify where the severity of multicolinearity was coming from. The whole cast metascore and whole cast user score averages as well as the MPAA rating R had the highest VIF quotients. After I removed those three features and ran the variance inflation factor test again all of the VIF quotients were below three and almost all of them were under 2.5 which provided some security that there was less colinearity. 

## Modeling 



## Conclusion




