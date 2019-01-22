# Moodie 
This application reads a logged in user's most recents timeline posts and, upon undergoing sentiment analysis, returns a list of movie recommendations. 

## Team Members 
* Jean P. Vazquez
* Kevin Chen
* Mohammed Uddin
* William He

## APIs Used
Three APIs were used in order to complete this project: 
```
1. Twitter API for user authentication and data, through a user's timeline, with which to generate movie recommendations.

2. IBMs Watson API for sentiment analysis which, when fed a user's timeline posts as the corpus, returns an analysis of a user's overall mood.

3. TMDB's proprietary API through which we searched for movies by their genre id which, using a homebrewed set of values, were correlated within the application to certain emotions. 
```

## Languages/Frameworks used in the project
Our application was built using the Django Web Framework with two main applications corresponding to the frontend and backend. Contained here are the sections of the project written, debugged, and deployed by me; this consists of the total backend for the application. Within the backend, Python was used for all API calls as well as a variety of python packages to both pass information from the frontend as well as grab information from the frontend. For the frontend, javascript with the React framework was used. 
