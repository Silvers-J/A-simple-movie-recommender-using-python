import pandas as pd
import numpy as np

class SimpleRecommender():
    '''
    This will simply recommend movies from a user
    who is similar(based on the movie ratings given) to you.
    '''

    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('movies.csv')

    recommendations = []


    def __init__(self, ratings_by_user):

        self.userRating = self.getUserList(ratings_by_user)
            
        self.ratings['rating'] *= 2
        
        self.M = self.ratings.pivot_table(index = ['userId'],
                                columns = ['movieId'],
                                values = 'rating')
        self.M.fillna(0)
        self.recommendations = self.getRecommendations(self.userRating) 


    
    def getUserList(self, ratings_by_user):
        '''
        Takes the input from the user as movie:rating pair
        '''
        userRatings = {}
        for title in ratings_by_user.split(','):

            key, value = title.split(':')

            key = self.movies.loc[self.movies['title'].str.startswith(key), 'movieId'].values[0]
        
            userRatings[key] = int(value)
    
        return userRatings


    def matchedList(self, userMovieList):
        '''
        This function will return list of users who have
        watched at least 4 movies same as user
        '''

        matched = {}
        for user in self.M.index:
        
            List = {}
            tempList = {}
        
            for movie in self.M.columns:
                if movie in userMovieList.keys():
        
                    if self.M[movie][user] > 0:
                
                        tempList[movie] = self.M[movie][user]
                        List.update(tempList)
                    
                        del tempList[movie]
                                    
                else:
                    continue
        
            matched[user] = List

        newDict = dict(matched)
    
        for keys in matched.keys():
            if not len(matched[keys]) > 3:
                del newDict[keys]

        return newDict


    def getRecommendations(self, userList):

        '''	
        Recommends movies from the list of user movies whose ratings
	were corealted with the input ratings
        '''
	
        match = self.matchedList(userList)
        corrset = {}

        for users, values in match.items():
            userRating = []
            dataRating = []

            for i, j in values.items():
                userRating.append(userList[i])
                dataRating.append(j)
                corrset[users] = self.corr(userRating, dataRating)

            bestcorr = max(corrset.values())
	 
        for key, value in corrset.items():
            if value == bestcorr:
                bestUser = key
	
        suggested_movie_ids = []
        suggested_movie_titles = []
		
        for i in self.M.columns:
            if self.M[i][bestUser] >= 10:
                suggested_movie_ids.append(i)

        for titles in self.movies['movieId']:
            if titles in suggested_movie_ids:
                suggested_movie_titles.append(self.movies.loc[self.movies['movieId'] == titles, 'title'].values[0])

        return suggested_movie_titles[:10]


    def corr(self, ListX, ListY):

        '''
        This function takes 2 lists as parameters and
        returns value of the coefficient of correalation
        between them
        '''
        
        meanX = np.mean(ListX)
        meanY = np.mean(ListY)

        ratingList = list(zip(ListX, ListY))

        numerator = 0.0
        sumx = 0.0
        sumy = 0.0

        for x, y in ratingList:

            numerator += (x - meanX) * (y - meanY)

            sumx += (x - meanX)**2

            sumy += (y - meanY)**2

            if not (sumx == 0 or sumy == 0):
                corr = numerator / pow(sumx * sumy, 0.5)

            else:
                corr = 0
        
        return corr

    def topMovies(self):
    
        top_movies = []
    
        for movie in self.M.columns:
            if self.M[movie].mean() >= 8.5 and self.M[movie].count() > 50:
                top_movies.append(movie)
            
        return top_movies[:10]







