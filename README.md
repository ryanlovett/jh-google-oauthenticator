# OAuthenticator

---
Notice: This code has been absorbed by [Jupyter's OAuthenticator](https://github.com/jupyter/oauthenticator). Please use that instead.

---

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

You will need to provide the OAuth callback URL and the Google OAuth client ID
and client secret to JupyterHub. For example, if these values are in the
environment variables `$OAUTH_CALLBACK_URL`, `$OAUTH_CLIENT_ID` and
`$OAUTH_CLIENT_SECRET`, you should add the following to your
`jupyterhub_config.py`:

    c.GoogleOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
    c.GoogleOAuthenticator.oauth_client_id = os.environ['OAUTH_CLIENT_ID']
    c.GoogleOAuthenticator.oauth_client_secret = os.environ['OAUTH_CLIENT_SECRET']

If you want to authenticate users in a hosted Google domain, e.g. `your-institution.edu`, use
`oauthenticator.GoogleAppsOAuthenticator` and add the following to your `jupyterhub_config.py`:

    c.GoogleOAuthenticator.hosted_domain = os.environ['HOSTED_DOMAIN']
    
and set the environment variable accordingly. This authenticator was developed to be used in an environment derived from
[compmodels](https://github.com/compmodels/jupyterhub-deploy) where spawned containers are named after users. Container names cannot contain `@' so this latter authenticator class will strip it off in addition to the hosted domain name.
