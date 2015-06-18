# OAuthenticator

Google OAuth 2.0 + JuptyerHub Authenticator = OAuthenticator

Google OAuthenticator is based on [GitHub OAuthenticator](https://github.com/jupyter/oauthenticator).

## Installation

First, install dependencies:

    pip install -r requirements.txt

Then, install the package:

    python setup.py install

## Setup

You will need to create an
[OAuth 2.0 client ID](https://developers.google.com/console/help/new/?hl=en_US#generatingoauth2)
in the Google Developers Console. A client secret will be automatically generated for you. Set the callback URL to:

    http[s]://[your-host]/hub/oauth2callback

where `[your-host]` is your server's hostname, e.g. `example.com:8000`.

Then, add the following to your `jupyterhub_config.py` file:

    c.JupyterHub.authenticator_class = 'oauthenticator.GoogleOAuthenticator'

You can alternatively use `LocalGoogleOAuthenticator` to handle both local and
GitHub auth.

You will need to provide the OAuth callback URL and the Google OAuth client ID
and client secret to JupyterHub. For example, if these values are in the
environment variables `$OAUTH_CALLBACK_URL`, `$OAUTH_CLIENT_ID` and
`$OAUTH_CLIENT_SECRET`, you should add the following to your
`jupyterhub_config.py`:

    c.GoogleOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
    c.GoogleOAuthenticator.oauth_client_id = os.environ['OAUTH_CLIENT_ID']
    c.GoogleOAuthenticator.oauth_client_secret = os.environ['OAUTH_CLIENT_SECRET']
