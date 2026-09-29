# Process book List Tuner - Hendrik Scheeres

This process book will be used to keep track of my progress during this project. I will mainly describe the most important findings and challenges I have encountered during the project.

The decisions I make will be documented as follows:

- The choice I’ve made
- What I expect to happen as a result of that choice (at this moment in time)
- Why I expect things to pan out that way

## Wednesday May 13 2020
Today I started on my prototype. First I organized my repository with the essential files and folders. A template folder for html templates, a static folder for stylesheets and scripts and python files for the server and database coordination. I also included a requirements.txt file and run.sh and prepared my application.py and models.py files so I was able to run my website (include FLASK and SQLAlchemy). The I started working on my main templates for my site.

To style the templates I organized my stylesheets in the styles folder. *main.scss* imports all the other scss files in the folder and is converted to *main.css* that is linked to on my html pages.
For all the extra plugins and frameworks I use in html decided to create a *style.html* file, that is included in all the other html files. This keeps the html files cleaner.

I managed to finish up the frontpage and playlistspage html and scss files and tomorrow I aim to finish up the statistics html file and start working with the Spotify API.

## Thursday May 14 2020
I first finished up the statisticspage html, so all my templates are ready.

## Friday May 15 2020
Today I am going to practice using the Spotify API. First I tried to use the API using only the documentation on the website. After encountering numerous authorization problems and discussing it with a TA, I decided to import an external library especially made for using the Spotify API on python ([spotipy](https://github.com/plamere/spotipy)).

With the help of Spotipy I managed to redirect the user to the Spotify authorization page. The only problem is that the page the user gets redirected from doesn't close of. I will try and save this later on in the project.

Besides that I had trouble saving the user token after the user was authenticated. So I tried using another Spotify API library to try to authenticate the user: [Tekore](https://pypi.org/project/tekore/). This sadly did not solve the problem, but only complicated things even more. As with Tekore, after the user authentication the redirect uri has to be pasted in the terminal to save the user token.

I aim to finish up the user authentication during my next session.

## Saturday May 16 2020

Today I decided to try another approach to the user authentication. Instead of using a Spotify API library I am going to experiment authorizing the user using a more known libraray with more documentation: [Authlib](https://docs.authlib.org/en/latest/flask/2/authorization-server.html)

This was sort of successful, I am now able to prompt the Spotify login page. Only I have to redesign how the user gets linked to the login route has the javascript request sadly doesn't work. And I have to check if I am able to access the data I need to access with the API and see how to refresh a token.

## Monday May 18 2020

I succeeded in logging in the user to the Spotify API and retrieving basic API information such as the username.

## Tuesday May 19 2020
Today I proceeded to work with the Spotify API. The frontpage and playlist page are as good as finished. There are some problems I have encountered:

- *The Spotify API has a max of 50 when it comes to loading user playlists.*

If I have enough time I might be able to create a next button on the playlists page that show the remaining amount of playlists.
Otherwise I will just have to put a disclaimer on the website that it goes up to 50 playlists per user.

- *The Spotify API has a max of 100 when it comes to loading track features.*

The easiest way to account for this is to disclaim that only playlists with 100 songs or fewer can be analyzed and then to exclude the playlists with 100+ songs from the playlist page. This shouldn't be to hard to implement.

Furthermore the playlist and statistics page are both accessible without being logged in. So I have to fix this as well. I am considering using flask login to achieve this. But first I want to finish visualizing the audio feature data on the statistics page.

Besides finishing the first versions of the frontpage I started figuring out how to organize the audio feature data. To do this I created the *Spotify.py* file, which contains different functions to organize the data and calculate the average. Tomorrow I will test the datasets on the website using chart.js.

## Wednesday May 20 & Thursday May 21 2020
The next step was to display the playlist statistics on my website with chart.js. This problem could be divided in different steps:

**Designing the charts**

  - **requesting all the necessary information from the Spotify API**
  In my last entry I specified that all the functions used to request the data from Spotify were stored in a Spotify.py file. The charts I wanted to display were:

    - *A linear chart with all the track features over the whole playlist*
    - *A linear chart with two y-axes: the tempo and loudness*
    - *A radar chart with the average track features*
    - *A doughnut chart with all the track genres.*

  First I figured out which data I would need from the Spotify API and then I had to format that information.

  - **formatting this information so it could be easily used**
  I structured the functions in Spotify.py to return a dictionary with all the necessary values that I could easily use with chart.js.

  One problem that occurred was that to get the genres of a track I had to get the all the track artists. But I was only able to request 50 artist at once using the Spotify API. A single track can have multiple artist, so the amount of artists increased rather quick. This in turn results in an incomplete genre data set.

  To solve this I decided to create a function that created chunks of 50 artist form the whole list of artists and requested the genre information per 50 artists. So the all the information was requested over multiple API requests and added together later on.

  Separating the functions that collected and formatted the needed data made it really easy to change small things later on in process.


  - **sending the information from my server to the javascript file that generates the chart**
  I tried different approaches to configure this. First I tried to convey the information in the html file of the statisticspage. However, the dataset was quite large and I seemed to be unable to correctly parse the information in my javascript file.

  The second and successful approach was to make an AJAX request from my javascript file to a separate pathway that collected and returned all the data to the javascript file. This made the process more clear.


  - **creating the charts**
  To create and organize the charts I created *chart_functions.js* were I saved each chart as a separate function. These functions were called once all the data was successfully loaded from the server.


**Remaining problems**
A few problems remained after completing the charts design:

  - *charts layout*

  To optimally display the playlist data I need to finetune the layout of the charts. This can be quite time consuming considering the fact that I not yet very familiar with the charts.js library.

  - *charts information*

  To improve the functionality of the website it would be quite useful to add some information about each chart and its parameters. I have not accounted for this in my design or proposal. So I will have to think it out from scratch.

  - *link to songs*

  As an extra, I think it would be really cool if the chart data could be linked to the specific song. So if you hover over the dots on the linear charts you can see which song the values belong to.


**Implementing the seal of approval**
To implement the seal of approval functionality I'll have to complete the following steps:

  - *create the user database with the playlists and their seals*
  - *create a function that compares the playlist data to that playlist data*
  - *create a pathway that automatically collects, formats and  returns this data*
  - *send the data from the server to the javascript file*
  - *correctly display the information*

After successfully creating the database and functions that extract the relevant playlist data it was time to compare the data values of the seal playlists and the users playlist.

However, comparing the data seemed more difficult than initially thought. Besides it would cost quite some time for a rather arbitrary statistical analysis. So instead of actually running any statistics I decided to simply plot the seal playlist data besides the current user data for comparison.

This in turn made me decide to not implement the "mark playlist approved" functionality, because the playlist will not actually be approved or disapproved by the web application.

Lastly I also decided not to implement the save button. After implementation of most of my project this did not seem to be a relevant functionality for the sites users.

Instead of spending time on these functionalities. I decided to spend more time on the charts and maybe implement smaller functionalities like links to the playlists or tracks.

## Friday May 22 2020

TO-DO list for today:
- fix pathways accessibility with user session **check**
- fix compare playlist section on the statisticspage
- fix track list dropdown on the statisticspage **check**
- display only playlist below 100 tracks on the playlistspage **check**
- remove save button **check**
- fine tune charts
- put client secret and client id in run.sh **check**
- create load animation
- add some more text to explain the function of the website.

## Monday May 25 2020

TO-DO list for today:
  - fix compare playlist section on the statisticspage **check**
  - create load animation
  - add some more text to explain the function of the website. **check**
  - finetuned the axes of the charts **check**
  - add colors to the charts
  - add labels for the axes
  - add dropdown logo to the navbar
  - fix the list in the compare section

Furthermore I added some useful links in the chart explanation sections:

- [Spotify API documentation](https://developer.spotify.com/documentation/web-API/reference/tracks/get-audio-features/)

Clearly explains the different track features.

- [Every noise at once map](http://everynoise.com/everynoise1d.cgi?vector=name&scope=all)

An easy to use website to browse different music genres on Spotify


## Tuesday May 26 2020

TO-DO list for today:
- create load animation
- add colors to the charts **check**
- add labels for the axes **check**
- add dropdown logo to the navbar **check**
- fix the list in the compare section **check**
- update layout of the statistics page **check**

To automatically generate the chart colors I used a chart.js plugin:
[Colorschemes](https://github.com/nagix/chartjs-plugin-colorschemes)

## Wednesday May 27 2020

TO-DO list for today:
- hover ticks in graphs **check**
- view all user playlists (so more than 50 per users) **check**
- explanation on the playlist page **check**
- fix song with no artist problem **check**
- create loading animation **check**

To create the loading animation I used [This website](https://projects.lukehaas.me/css-loaders/) to generate css and html code for the loading animation.


Code cleanup:
  - application.py **check**
  - Spotify.py **check**
  - models.py **check**
  - run.sh **check**
  - templates
    - frontpage.html **check**
    - navbar.html **check**
    - playlistpage.html **check**
    - statisticspage.html **check**
    - style.html **check**
  - static
    - scripts
      - chart.js **check**
      - chart_functions.js **check**
    - styles
      - frontpage.scss
      - general.scss
      - main.scss
      - navbar.scss
      - playlistspage.scss
      - statisticspage.scss
      - variables.scss

## Thursday May 29 2020

TO-DO list for today:
  - Finish code cleanup:
    - styles
      - frontpage.scss **check**
      - general.scss **check**
      - main.scss **check**
      - navbar.scss **check**
      - playlistspage.scss **check**
      - statisticspage.scss **check**
      - variables.scss **check**

  - add error pathways:
    - charts errorpages **check**
    - template errorpages **check**
