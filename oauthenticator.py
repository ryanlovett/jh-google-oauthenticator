"""
Custom Authenticator to use Google OAuth with JupyterHub.

Derived from GitHub OAuth authenticator,
https://github.com/jupyter/oauthenticator

"""

import os
import binascii
import json

from tornado            import gen
from tornado.auth       import GoogleOAuth2Mixin
from tornado.escape     import to_unicode
from tornado.web        import HTTPError

from IPython.utils.traitlets import Unicode

from jupyterhub.handlers import BaseHandler
from jupyterhub.auth     import Authenticator, LocalAuthenticator
from jupyterhub.utils    import url_path_join

class GoogleLoginHandler(BaseHandler, GoogleOAuth2Mixin):
	def get(self):
		guess_uri = '{proto}://{host}{path}'.format(
			proto=self.request.protocol,
			host=self.request.host,
			path=url_path_join(self.hub.server.base_url, 'oauth_callback')
		)

		redirect_uri = self.authenticator.oauth_callback_url or guess_uri
		self.log.info('oauth redirect: %r', redirect_uri)

		self.authorize_redirect(
			redirect_uri=redirect_uri,
			client_id=self.authenticator.oauth_client_id,
			scope=['openid', 'email'],
			response_type='code')

class GoogleOAuthHandler(BaseHandler, GoogleOAuth2Mixin):
	@gen.coroutine
	def get(self):
		self.settings['google_oauth'] = {
			'key': self.authenticator.oauth_client_id,
			'secret': self.authenticator.oauth_client_secret,
			'scope': ['openid', 'email']
		}

		# TODO: Check if state argument needs to be checked
		#state = to_unicode(self.get_secure_cookie('openid_state'))
		#if not state == self.get_argument('state', False):
		#	raise HTTPError(400, "Invalid state")

		username = yield self.authenticator.authenticate(self)
		if username:
			user = self.user_from_username(username)
			self.set_login_cookie(user)
			self.redirect(url_path_join(self.hub.server.base_url, 'home'))
		else:
			# todo: custom error page?
			raise HTTPError(403)

class GoogleOAuthenticator(Authenticator):

	login_service = "Google"
	ACCESS_TOKEN_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
	oauth_callback_url = Unicode('', config=True)
	oauth_client_id = Unicode(os.environ.get('OAUTH_CLIENT_ID', ''),
		config=True)
	oauth_client_secret = Unicode(os.environ.get('OAUTH_CLIENT_SECRET', ''),
		config=True)

	def login_url(self, base_url):
		return url_path_join(base_url, 'oauth_login')
	
	def get_handlers(self, app):
		return [
			(r'/oauth_login', GoogleLoginHandler),
			(r'/oauth2callback', GoogleOAuthHandler),
		]
	
	@gen.coroutine
	def authenticate(self, handler):
		code = handler.get_argument('code', False)
		if not code:
			raise HTTPError(400, "oauth callback made without a token") 

		user = yield handler.get_authenticated_user(
			redirect_uri=self.oauth_callback_url,
			code=code)
		access_token = str(user['access_token'])

		http_client = handler.get_auth_http_client()

		response = yield http_client.fetch(
			self.ACCESS_TOKEN_URL + '?access_token=' + access_token
		)

		if not response:
			self.clear_all_cookies()
			raise HTTPError(500, 'Google authentication failed')

		bodyjs = json.loads(response.body.decode())

		username = bodyjs['email']
		if self.whitelist and username not in self.whitelist:
			username = None
		raise gen.Return(username)

class GoogleAppsOAuthenticator(GoogleOAuthenticator):

	apps_domain = Unicode(os.environ.get('APPS_DOMAIN', ''), config=True)

	@gen.coroutine
	def authenticate(self, handler):
		username = yield GoogleOAuthenticator.authenticate(self, handler)

		if not username or username.endswith('@'+self.apps_domain):
			username = None
		else:
			username = username.split('@')[0]

		raise gen.Return(username)

class LocalGoogleOAuthenticator(LocalAuthenticator, GoogleOAuthenticator):
	"""A version that mixes in local system user creation"""
	pass

class LocalGoogleAppsOAuthenticator(LocalAuthenticator, GoogleAppsOAuthenticator):
	"""A version that mixes in local system user creation"""
	pass
