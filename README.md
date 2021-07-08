Capstone Three: Using a Deep Neural Network to Build a Movie Recommendation System
==============================
The third capstone project for Springboard's Data Science track.

Author: Sahar Manavi

smanavi.ctp [at] gmail [dot] com

Problem Statement
-----------------
MUBI is a self-described database and streaming service for auteur cinema. It’s currently hand-curated, but as its user base grows, the task of hand curating films for hundreds of thousands of users starts to become tenuous. While hand curation is a feature of MUBI that sets it apart from other streaming services (in addition to its quirky range of films in its library), there might be a way to assist the hand curation.

What if there was an automated recommendation system that could narrow the pool of potential movies the user might want to watch? This way, the system could predict, for instance, 5 movies, and a hand curator could choose to recommend up to 4 of those 5, having more confidence in the recommendation with less upfront work.

Project Overview
-----------------
Dataset is from https://www.kaggle.com/clementmsika/mubi-sqlite-database-for-movie-lovers

I built a deep feed-forward neural network as part of an educational project to predict what movies a user might like based on all users' ratings. The final version takes in a user id and returns a list of up to 20 highly rated (4/5 or above) movies particular to that user. Going forward, this dataset and model would be much better suited to be presented as a dashboard. For now, there is a Jupyter notebook serving as an entry point (details below).

Acknowledgements
-----------------
While the research for this project spanned multitudes, there was one particular post that was pivotal in my understanding and implementation of a DNN for a recommender system: Rising Odegua's Heartbeat post, found here: https://heartbeat.fritz.ai/build-train-and-deploy-a-book-recommender-system-using-keras-tensorflow-js-b96944b936a7

I am also very grateful for Tensorflow's extensive documentation and tutorials.

Finally, my warmest, deepest gratitude goes to Travis Hall, who lent me the use of the many, many CPUs I needed via a virtual machine. This literally would not have been possible without his assistance.

Interact With the Project!
-----------------
The "Interactive Example" folder is meant to display the types of recommendations the system can generate. It uses a pre-generated recommendation dataset to avoid complications around downloading and running the model itself (though everything needed to run the model is present on this repository, should you wish to do so).

To see one set of results, simply open the "Explore Model Results.ipynb" notebook in GitHub and you will see a pre-run example.

You can also download the contents of the entire Interactive Example folder to your local machine to play with examples yourself. The notebook guides you through the databases and libraries you need (not many) to make it run.

This was an educational project with limited time and resource investment possible. However, if it inspires you, please feel free to fork the repo and make your own additions and changes.
