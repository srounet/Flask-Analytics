from __future__ import absolute_import

from datetime import datetime, timedelta
from hashlib import sha1
from urlparse import urlparse
from uuid import uuid4
import hmac

from flask import _request_ctx_stack, current_app, session

COOKIE_NAME = 'analytics'
COOKIE_DURATION = timedelta(days=365)


def _cookie_digest(payload, key=None):
    if key is None:
        key = current_app.config["SECRET_KEY"]
    payload = payload.encode("utf8")
    mac = hmac.new(key, payload, sha1)
    return mac.hexdigest()


def _get_cookie(request):
    config = current_app.config
    cookie_name = config.get("ANALYTICS_COOKIE_NAME", COOKIE_NAME)
    request_cookie = request.headers['cookie']
    cookies = request_cookie.split(';')
    for cookie_data in cookies:
        if cookie_name in cookie_data:
            name, value = cookie_data.split('=')
            return value
    return None


class Analytics(object):

    analytics_callback = None

    def __init__(self, app):
        self.app = app
        self.cookie_value = None
        if self.app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['analytics'] = self
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def analytics_process(self, callback):
        self.analytics_callback = callback

    def before_request(self):
        ctx = _request_ctx_stack.top
        cookie_value = _get_cookie(ctx.request)
        if cookie_value:
            self.cookie_value = cookie_value
        self.track_request(ctx.request)

    def after_request(self, response):
        config = current_app.config
        cookie_name = config.get("ANALYTICS_COOKIE_NAME", COOKIE_NAME)
        self._set_tracker(response)
        return response

    def _set_tracker(self, response):
        if self.cookie_value:
            return
        config = current_app.config
        name = config.get("ANALYTICS_COOKIE_NAME", COOKIE_NAME)
        domain = config.get("ANALYTICS_COOKIE_DOMAIN", None)
        duration = config.get("ANALYTICS_COOKIE_DURATION", COOKIE_DURATION)
        data = _cookie_digest(str(uuid4()))
        expires = datetime.now() + duration
        response.set_cookie(name, data, expires=expires, domain=domain)

    def track_request(self, request):
        parse_result = urlparse(request.url)
        static_url_path = current_app.static_url_path
        analytics = {
            'args': request.args,
            'charset': request.url_charset,
            'url': request.url,
            'user_agent': request.user_agent,
            'cookie': self.cookie_value,
            'is_static': parse_result.path.startswith(static_url_path),
            'blueprint': request.blueprint,
            'view_args': request.view_args,
            'remote_addr': request.remote_addr,
        }
        self.analytics_callback(analytics)
