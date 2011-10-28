from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import simplejson as json
#import json
import random
import urlparse
import cgi
import urllib

def _parse_access_token(token):
    app_id, session_key, _ = token.split("|")
    _, uid = session_key.split("-")
    app_id = int(app_id)
    uid = int(uid)
    return app_id, uid

def _generate_profile(uid):
    # is random.seed thread safe? Or is it per-process?
    random.seed(uid)
    profile = {'id': uid,
               'first_name': _random_string(8),
               'last_name': _random_string(8),
               'email': str(uid) + "@this-is-not-a.domain",
               'gender': random.choice(["male", "female"]),
               'birthday': str(random.choice(range(1,12))) + "/" + str(random.choice(range(1,30))) + "/" + str(random.choice(range(1960,2000))),
               }
    profile['name'] = profile['first_name'] + " " + profile['last_name']
    return profile

def _random_string(len):
    s = ""
    while len:
        s += chr(random.choice(range(ord("a"), ord("z"))))
        len -= 1
    return s

def _generate_friends(uid):
    random.seed(uid)
    num = random.choice(range(5,100))
    friends = []
    while num:
        friend_id = random.randint(1000000, 500000000)
        friends.append(_generate_profile(friend_id))
        num -= 1
    return friends

def _generate_likes(uid):
    random.seed(uid)
    num = random.choice(range(5,100))
    likes = []
    while num:
        like_id = random.randint(1000000, 500000000)
        likes.append({'id': like_id})
        num -= 1
    return likes

class Authorize(webapp.RequestHandler):
    def get(self):
        client_id = self.request.get('client_id')
        page = """
        <html>
        <body>
        Please log in:<br/>
        <form method="post">
        Email: <input type="text" name="email"/><br/>
        Password: <input type="password" name="password"/><br/>
        <input type="hidden" name="client_id" value="%s"/>
        <button type="submit">submit</button>
        </form>
        </body>
        </html>
        """ % (client_id)
        self.response.headers['Content-type'] = 'text/html'
        self.response.out.write(page)

    def post(self):
        email = self.request.get('email')
        uid, _ = email.split("@")
        app_id = self.request.get('client_id')
        code = uid
        redirect_url = self.request.get('redirect_uri')
        parsed_url = urlparse.urlparse(redirect_url)
        query_dict = cgi.parse_qs(parsed_url.query)
        query_dict['code'] = code
        redirect_url = urlparse.urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, urllib.urlencode(query_dict), ''))
        self.redirect(redirect_url)

class AccessToken(webapp.RequestHandler):
    def _generage_access_token(self, uid, app_id):
        session_key = "random-" + uid
        access_token = app_id + "|" + session_key + "|xyz"
        return access_token

    def get(self):
        uid = self.request.get('code')
        app_id = self.request.get('client_id')
        access_token = self._generage_access_token(uid, app_id)
        self.response.headers['Content-type'] = 'text/plain'
        self.response.out.write("access_token=" + access_token)

class MyProfile(webapp.RequestHandler):
    def get(self):
        app_id, uid = _parse_access_token(self.request.get("access_token"))
        profile = _generate_profile(uid)
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(profile))

class MyLikes(webapp.RequestHandler):
    def get(self):
        app_id, uid = _parse_access_token(self.request.get("access_token"))
        likes = {'data': _generate_likes(uid)}
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(likes))

class FriendLikes(webapp.RequestHandler):
    def get(self, user_id):
        app_id, uid = _parse_access_token(self.request.get("access_token"))
        likes = {'data': _generate_likes(uid)}
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(likes))

class MyFriends(webapp.RequestHandler):
    def get(self):
        app_id, uid = _parse_access_token(self.request.get("access_token"))
        friends = {'data': _generate_friends(uid)}
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(friends))

class MyPicture(webapp.RequestHandler):
    def get(self):
        self.redirect("http://this-is-not.a.domain/foo.jpg")

application = webapp.WSGIApplication(
    [('/oauth/authorize', Authorize),
     ('/oauth/access_token', AccessToken),
     ('/me', MyProfile),
     ('/me/likes', MyLikes),
     ('/([0-9]+)/likes', FriendLikes),
     ('/me/friends', MyFriends),
     ('/me/picture', MyPicture)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
