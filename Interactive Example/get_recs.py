import pandas as pd
import numpy as np
import json
import random

def print_or_return(func):
    '''
    Decorator to allow flexible usage of functions. Can either print or return values using parameter print_or_return.
    '''
    def print_return_wrapper(self, print_or_return=None, *args, **kwargs):
        if print_or_return==None:
            print_or_return='print'
        text, value = func(self, print_or_return, *args, **kwargs)
        if print_or_return=='print':
            if isinstance(text, list):
                for line in text:
                    print(line)
            else:
                print(text)
        elif print_or_return=='return':
            return value
    return print_return_wrapper


class GetRecommendations():
    """
    Get movie recommendations for MUBI users from a pre-generated database of recommendations made by a NN-trained model.
    Responses will be printed out unless print_or_return parameter in functions is set to 'return'.

    Methods
    ----------
    get_started()
    establish_user_stats()
    get_user_mean()
    get_recs()
    get_user_top_movies()
    get_user_bottom_movies()
    get_user_model_performance()
    get_user_n_reviews()
    """

    def __init__(self, MUBI_user_id='random', recommendations='use_short', print_welcome=True):
        '''
        Parameters
        ----------
        MUBI_user_id: str
            Either the user_id from the MUBI database, or "random" to get the information for a random user.
            default = 'random'
        recommendations: {'use_short', 'use_long'}
            'use_short' to load the small library of 10 uses on Google Sheets, or 'use_long' if you've downloaded the csv with recommendations
            for 1000 users.
            default = 'use_short'
        print_welcome: bool
            Whether or not to print the welcome text when the class is initiated.
            default = True
        '''

        self.ratings_URL = r"https://docs.google.com/spreadsheets/d/1olKN3RWDIFGG1cQ6NA8x_26PpFJ8Umu31GfzSvgGfvs/export?format=csv&gid=121740241"
        self.suggestions_URL = r"https://docs.google.com/spreadsheets/d/1dY-Bj_1P0YavMa-e7F37MtR8Y10ZpyhPuUK91M7z5JU/export?format=csv&gid=1293929908"
        if print_welcome==True:
            print("Hello! This class will load two Google Sheets in addition to the JSON file downloaded with the script and notebook.")
            print("If you wish, you can inspect the sheets prior to beginning at the following urls:")
            print("https://docs.google.com/spreadsheets/d/1olKN3RWDIFGG1cQ6NA8x_26PpFJ8Umu31GfzSvgGfvs/edit#gid=121740241")
            print("https://docs.google.com/spreadsheets/d/1dY-Bj_1P0YavMa-e7F37MtR8Y10ZpyhPuUK91M7z5JU/edit#gid=1293929908")
            print()
            print("You may also download and use the csv with suggestions for 1000 users. The URL for that is here:")
            print(r"https://drive.google.com/file/d/1URuF9NYKas5pZPqYcxlx5QeCBOtbqa_w/view?usp=sharing")

        self.recommendations = recommendations
        self.uid = MUBI_user_id

    def get_started(self):
        '''
        Loads necessary dataframes (from Google sheets or local) and dictionaries (from local).
        '''
        print("This might take a few minutes depending on your internet connection.")
        try:
            with open('translation_dict.json', 'r') as f:
                self.translation_dict = json.load(f)
        except FileNotFoundError:
            print("Please move the translation_dict.json file to the same folder as this notebook.")

        self.unique_movies = range(89418)
        self.ratings_df = pd.read_csv(self.ratings_URL, sep=',', header=0, index_col=0)

        if self.recommendations=='use_short':
            self.suggestions_df = pd.read_csv(self.suggestions_URL, index_col=0).T
            # self.suggestions_df = suggestions_df.rename(columns={'10110.1':'10110'}).T
        else:
            try:
                self.suggestions_df = pd.read_csv('user_recs.csv', index_col=0)
            except FileNotFoundError:
                print("Please move the user_recs.csv file to the same folder as this notebook.")

        self.establish_user_stats(self.uid)

    def establish_user_stats(self, user):
        '''
        Sets class instance of user. Can be rerun to view information for a new user without reinstanciating entire class.
        '''
        if self.recommendations=='use_short':
            self.user_list = [30637830, 43744268, 32627933, 51927810, 50184113]
        else:
            self.user_list = list(self.translation_dict['userid_to_user'].keys())

        if user=='random':
            self.user_id = random.choice(self.user_list)
            self.user = int(self.translation_dict['userid_to_user'][str(self.user_id)])
        else:
            self.user_id = user
            self.user = int(self.translation_dict['userid_to_user'][str(user)])

        self.user_ratings = self.ratings_df[self.ratings_df.user==self.user]
        self.suggested_ratings = self.suggestions_df.loc[str(self.user)]


    def _movie_to_title(self, movie_number):
        '''
        Translate movie number to title.
        '''
        movie_id = self.translation_dict['movie_to_id'][str(movie_number)]
        title = self.translation_dict['id_to_title'][str(movie_id)]
        return title

    def _is_close_enough(self, pred, ratings):
        '''
        Determine accuracy of predicted ratings.
        '''
        val = []
        for pair in zip(pred, ratings):
            if pair[1] == 5:
                val.append(pair[1] - 1 <= pair[0])
            else:
                val.append(pair[1] - .5 <= pair[0] <= pair[1] + .5)
        return val

    @print_or_return
    def get_user_mean(self, print_or_return=None):
        '''
        Get this user's mean value for actual ratings.
        '''
        if print_or_return==None:
            print_or_return='print'
        mean = np.round(self.user_ratings.rating_score.mean(), 1)
        text = "This user's average rating is {}.".format(mean)
        return text, mean

    @print_or_return
    def get_recs(self, print_or_return=None, n_recs=5):
        '''
        Get highly rated recommendations for user. Picks not-rated movies at random and sorts to return highest rated options.

        Parameters
        ----------
        n_recs: int
            The number of recommendations to return between [1, 20].
            default = 5
        '''
        if (n_recs > 20) or (n_recs < 1):
            print("Oops, that number of recs is out of range. Please pick an integer between 1 and 20.")
            return
        has_seen = self.user_ratings.movie.values
        movies_to_eval = random.choices(self.unique_movies, k=100)
        movies_to_eval = [m for m in movies_to_eval if m not in has_seen]

        if len(movies_to_eval) != 100:
            still_need = 100 - len(movies_to_eval)
            extras = random.choices(self.unique_movies, k=still_need)
            for e in extras:
                if (e not in movies_to_eval) and (e not in has_seen):
                    movies_to_eval.append(e)
                else:
                    continue

        rates = self.suggested_ratings.values[movies_to_eval]
        movie_indx = movies_to_eval
        movies = [self._movie_to_title(m) for m in movie_indx]
        movies_ratings = list(zip(movies, rates))
        movies_ratings.sort(key=lambda x: x[1], reverse=True)

        text = []
        for pair in movies_ratings[:n_recs]:
            text.append("Suggestion: {}. Estimated rating: {}.".format(pair[0], np.round(float(pair[1]), 1)))

        return text, movies_ratings[:n_recs]

    @print_or_return
    def get_user_top_movies(self, print_or_return=None, n=10):
        '''
        Return some of the user's highest rated movies.

        Parameters
        ----------
        n: int
            The number of top movies to return. If n is greated than the number of user's reviews, n will default to n_reviews.
            default = 10
        '''
        ranks = self.user_ratings.sort_values(by='rating_score', ascending=False)
        if len(ranks) < n:
            n = len(ranks)
        if len(ranks[ranks.rating_score==5]) > n:
            inds = random.choices(ranks[ranks.rating_score==5].index, k=n)
            movies = ranks.movie.loc[inds].values
            rates = ranks.rating_score.loc[inds].values
        else:
            movies = ranks.movie.values[:n]
            rates = ranks.rating_score.values[:n]
        titles = [self._movie_to_title(m) for m in movies]

        text = ["Here are {} of this user's top rated movies:".format(n)]
        for pair in list(zip(titles, rates)):
            text.append("{}  ({}/5)".format(pair[0], pair[1]))

        return text, list(zip(titles, rates))

    @print_or_return
    def get_user_bottom_movies(self, print_or_return=None, n=10):
        '''
        Return some of the user's lowest rated movies.

        Parameters
        ----------
        n: int
            The number of bottom movies to return. If n is greated than the number of user's reviews, n will default to n_reviews.
            default = 10
        '''
        ranks = self.user_ratings.sort_values(by='rating_score', ascending=True)
        if len(ranks) < n:
            n = len(ranks)
        if len(ranks[ranks.rating_score==1]) > n:
            inds = random.choices(ranks[ranks.rating_score==1].index, k=n)
            movies = ranks.movie.loc[inds].values
            rates = ranks.rating_score.loc[inds].values
        else:
            movies = ranks.movie.values[:n]
            rates = ranks.rating_score.values[:n]
        titles = [self._movie_to_title(m) for m in movies]


        text = ["Here are {} of this user's lowest rated movies:".format(n)]
        for pair in list(zip(titles, rates)):
            text.append("{}  ({}/5)".format(pair[0], pair[1]))

        return text, list(zip(titles, rates))

    @print_or_return
    def get_user_model_performance(self, print_or_return=None):
        '''
        Return the model accuracy for this particular user.
        '''
        has_seen = self.user_ratings.movie.values

        user_pred = self.suggested_ratings.iloc[has_seen].values
        user_ratings = self.user_ratings.rating_score.values
        vals = self._is_close_enough(user_pred, user_ratings)
        acc = np.round((sum(vals) / len(user_pred))*100, 2)
        text = "This user's predictions were accurate {}% of the time.".format(acc)

        return text, acc

    @print_or_return
    def get_user_n_reviews(self, print_or_return=None):
        '''
        Get the number of reviews this user has on record.
        '''
        n_reviews = len(self.user_ratings)
        text = "This user has {} reviews on record.".format(n_reviews)
        return text, n_reviews
