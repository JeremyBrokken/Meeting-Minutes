from MMwebsite import create_app #use create app from __init__.py

app = create_app()

if __name__ == '__main__': #run web server only if this file is selected
    #app.run = run flask application, start up a web server
    app.run(debug=True) #debug = true >>if changes made to python file, web server will update
            #debug to be turned off in production.

