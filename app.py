import flask
import logging
import mwoauth
import os
import yaml

app = flask.Flask(__name__)

# Load configuration from YAML file
__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))

@app.route('/')
def index():
    greeting = app.config['GREETING']
    username = flask.session.get('username', None)
    return flask.render_template(
        'index.html', username=username, greeting=greeting)

@app.route('/login')
def login():
    consumer_token = mwoauth.ConsumerToken(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    try:
        redirect, request_token = mwoauth.initiate(
            app.config['OAUTH_MWURI'], consumer_token)
    except Exception:
        app.logger.exception('mwoauth.initiate failed')
        return flask.redirect(flask.url_for('index'))
    else:
        flask.session['request_token'] = dict(zip(
            request_token._fields, request_token))
        return flask.redirect(redirect)

@app.route('/results', methods=['POST'])
def receiveData():
    glam1 = request.form['glam_name']
    id = request.form['uuid']
    categories = categories
    glam_list = listOfGlams
    
    try:
        for glam in glam_list: 
            if glam['name'] == glam1:
    	        break
    except:
        return "GLAM Not Found in our list"

    #upload the image
    howManyMatches = main(uuid, categories)
    print('passes main')
    if howManyMatches == 0:
        return 'No match found!'
    else:
        returnString = 'operation successful'
    return returnString


@app.route('/oauth-callback')
def oauth_callback():
    """OAuth handshake callback."""
    if 'request_token' not in flask.session:
        flask.flash(u'OAuth callback failed. Are cookies disabled?')
        return flask.redirect(flask.url_for('index'))

    consumer_token = mwoauth.ConsumerToken(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])

    try:
        access_token = mwoauth.complete(
            app.config['OAUTH_MWURI'],
            consumer_token,
            mwoauth.RequestToken(**flask.session['request_token']),
            flask.request.query_string)

        identity = mwoauth.identify(app.config['OAUTH_MWURI'], consumer_token, access_token)
    except Exception:
        app.logger.exception('OAuth authentication failed')

    else:
        flask.session['access_token'] = dict(zip(
            access_token._fields, access_token))
        flask.session['username'] = identity['username']

    #return flask.render_template('glam_form.html') 
    return flask.redirect(flask.url_for('index'))


@app.route('/logout')
def logout():
    """Log the user out by clearing their session."""
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))

