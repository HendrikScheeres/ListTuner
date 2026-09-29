# Code review List Tuner - Hendrik Scheers

**My code was reviewed by Jesse Pannekeet**

## Review points I worked out

- **For reoccurring colours in your scss files you use sass variables, maybe you should check if you could use it for other variables as well. For example you use the 20px margin a lot.**

I could indeed have used more features of sass to make my css files more clear. The example given in the review comment is already a great example were I could of done this. Other examples would be to create standard variables for the width of the div borders or to use sass inheritance to style similar buttons such as the "ANALYZE" and "NEXT" playlist buttons.

- **Your "/logout" route seems more cumbersome than it needs to be. Instead of checking if the token is not in session, it might be easier to check if the token is in the session and if so: remove all the keys from the session.**  

Code example

        @app.route("/logout")
        def logout():
            ''' Logs the user out '''

            # check if a user is logged in
            if "token" not in session:
                return redirect(url_for("frontpage"))

            # remove all session keys
            for key in list(session.keys()):
                session.pop(key)

            return redirect(url_for("frontpage"))


I completely overlooked this! The first part of the code was indeed written to check if a token was in the session before removing all tokens from the session preventing an error from occurring. But it would indeed be more logical to write it like this:


        @app.route("/logout")
        def logout():
            ''' Logs the user out '''

            # check if a user is logged in
            if "token" in session:

                # remove all session keys
                for key in list(session.keys()):
                    session.pop(key)

            return redirect(url_for("frontpage"))

I tested it and it also worked (reverted it afterwards).



- **The name "seals" and thereby the purpose of your database is not very clear at first sight. So you might want to add a comment or something to fix this.**

I chose the name "seals" while I was still planning on implementing the "seal of approval" feature. After deciding it would be to cumbersome to create, I forgot to adjust the database accordingly. So to make the purpose of the database more clear it would have been smart to comment this better in my models.py file or to change the table name altogether. I more suiting name would have been "compare_playlists".


## Other review points

While reviewing Jesse's code I noticed had put all is python code in one "code" directory. This made his repository look very well organized. In following projects I might consider doing a similar thing.
