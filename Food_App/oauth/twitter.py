from flask import flash, redirect, url_for
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_login import current_user, login_user
from sqlalchemy.orm.exc import NoResultFound

from .. import db
from ..models import OAuth, User

blueprint = make_twitter_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def twitter_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with twitter.", category="error")
        return False

    resp = blueprint.session.get("account/verify_credentials.json")
    if not resp.ok:
        msg = "Failed to fetch user info from twitter."
        flash(msg, category="error")
        return False

    twitter_info = resp.json()
    twitter_user_id = str(twitter_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name, provider_user_id=twitter_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        twitter_user_login = str(twitter_info["screen_name"])
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=twitter_user_id,
            provider_user_login=twitter_user_login,
            token=token,
        )

    # Now, figure out what to do with this token. There are 2x2 options:
    # user login state and token link state.

    if current_user.is_anonymous:
        if oauth.user:
            # If the user is not logged in and the token is linked,
            # log the user into the linked user account
            login_user(oauth.user)
            flash("Successfully signed in with twitter.")
        else:
            # If the user is not logged in and the token is unlinked,
            # create a new local user account and log that account in.
            # This means that one person can make multiple accounts, but it's
            # OK because they can merge those accounts later.
            user = User(username=twitter_info["screen_name"])
            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)
            flash("Successfully signed in with twitter.")
    else:
        if oauth.user:
            # If the user is logged in and the token is linked, check if these
            # accounts are the same!
            if current_user != oauth.user:
                # Account collision! Ask user if they want to merge accounts.
                url = url_for("auth.merge", username=oauth.user.username)
                return redirect(url)
        else:
            # If the user is logged in and the token is unlinked,
            # link the token to the current user
            oauth.user = current_user
            db.session.add(oauth)
            db.session.commit()
            flash("Successfully linked twitter account.")

    # Indicate that the backend shouldn't manage creating the OAuth object
    # in the database, since we've already done so!
    return False


# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def twitter_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")
