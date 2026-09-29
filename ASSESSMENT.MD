# Assessment List Tuner - Hendrik Scheeres


## Highlights

**Code**

- I am proud of the organization of my stylesheets. This made it very easy to keep oversight and to adjust small things to the webdesign.
- I really liked working with a separate file with functions to make API requests and format the requested data (spotify.py)
- I don't know if this was the best way to do this, but using one html template for all the plugins and addons helped me clear up the other html files (style.html)
- I am satisfied with how simple I managed to keep the OAuth with Authlib (shoutout to Marijn). And in turn this helped me to keep my application.py rather simple.
- I still like using run.sh to start up the application with all the necessary environment variables (shoutout to Quinten)


**Interaction design**

- I am proud of the fact that my website design resembles my initial design on paper quite a lot. I also like its simplicity and color scheme.
- Experimenting with the Chart.js plugin and the interactive charts was really fun and informative!
- I also had fun while adding some extra's at the end of my project. For example the track preview function or the loading animations.
- It was challenging to come up with the error handling of my application. What I made is definitely not perfect, but it does feel good to have some kind of safety net.



## Important decisions

- Stepping away from Spotify API specific libraries such as *spotipy* and *tekore* to only use *Authlib*:

I'm glad realized early on while working with these libraries that they were quite cumbersome and made for very specific tasks for the API. Moving on to *Authlib* wasn't only better for my project, but I now have an general idea how handle the authorization of all kinds of API's (instead of only the Spotify API).



- Filtering out playlists with 100 tracks or more from the playlistspage.

While deciding not to do this it almost felt like giving up on a problem, as I did manage to overcome other limits of the Spotify API requests. Yet, in hindsight it would not have been very useful to waste too much time on this as most of the charts were already quite complicated below 100 tracks. This made me realize that it is not always a bad thing to set limits to your application. In this way you can focus on other important aspects of your project.



- Adjusting the function of the "seal of approval" feature and removing the "save as pdf" feature.

Adjusting/removing these features gave me the opportunity to focus on more achievable and relevant features of my web application.
