# thefakebook
## Overview

Fakebook provides an implementation of the Facebook Graph API in order to test Facebook Connect applications. It's difficult to impossible to create many test users on the real Facbeook. Instead, Fakebook makes it easy to simulate a nearly infinite number of users.

This is an very incomplete project, but it has been helpful for me in doing load testing.

All of the data returned is randomly generated. The same data will be returned for subsequent calls using the same auth_token, but the data itself (names, likes, friends etc) is all random.

The code is designed to run on Google App Engine, though porting to a different environment like Django should be trivial.

## Usage

* Upload this code to your App Engine instance.
* Change your app to point to your App Engine URL instead of to facebook.com
* Log your test users in as 999@foo.bar where 999 is the whatever numeric Facebook UID you want to assign to that user. Logging in as the same UID in the future will generate the same test data as prior logins (first name, email address etc). No password is required.


## Status

* Basic Facebook Connect OAuth flow works
* The following API calls are implemented:
  * /oauth/authorize
  * /oauth/access_token
  * /me
  * /me/friends
  * /me/likes
  * /me/picture
* No error handling. Just get a Python exception if you pass invalid inputs.

## To Do
* Support more API calls
* Support pre-loading data that is to be returned instead of generating random data
* Error handling in the Fakebook code itself
* Error injection to test error handling in your app
