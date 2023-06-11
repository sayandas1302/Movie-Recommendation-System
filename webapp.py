# required libraries
from flask import Flask, render_template, request
import pandas as pd

# calling required datsets
df = pd.read_csv('./dataset/preProcessed.csv')
similarity_score = pd.read_csv('./dataset/similarity_score.csv')
popular = pd.read_csv('./dataset/top_50_movies.csv')

# the recommendation function
def recommender(movie_name):
    idx = list(df[df['title'] == movie_name].index)[0] 
    score = similarity_score.iloc[idx,:].sort_values(ascending=False)
    recom_movie_idx = score.index[1:11].astype('int')
    recom_movie_detail = df.loc[recom_movie_idx, ]
    return recom_movie_detail

# the flask app
app = Flask(__name__)

# the flask functionality
@app.route('/', methods=['GET', 'POST'])
def index():
    choice = "Select the movie you have watched"
    sugg = None
    if request.method == 'POST':
        choice = request.form.get('movieName')
        if choice is not None:
            sugg = recommender(choice)
        else:
            choice = "Select the movie you have watched"
            sugg = None
    return render_template('template.html', 
                           choice=choice,
                           movies=df['title'].sort_values(),
                           sugg=sugg,
                           pop=popular)

if __name__ == '__main__':
    app.run(debug=True)