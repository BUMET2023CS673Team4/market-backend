# from user.py
# session returns user id
# this py file is to check whether the user id is in the session
# if yes, return the user id and email
# if no, return error to frontend
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from fleaapi.models import User
import json
import logging
from django.views.decorators.http import require_GET


# when successfully login, the user id is in the session
'''
 if user is not None:
            # Successful login
            logger.info(f"[login] user {email} logged in successfully")
            request.session["user_id"] = user.id
            return redirect("/")  # send user to home page on successful login
            '''


# using login function in user.py to login


def session(request: HttpRequest) -> HttpResponse:
    """
    if login successfully, the user id is in the session
    return the user name and email
    """
    logger = logging.getLogger(__name__)
    logger.info("[session] flow started")

    # check whether the user id is in the session
    user_id = request.session.get('user_id')
    print
    if not user_id:
        logger.error(f"[session] user is not logged in")
        return HttpResponseBadRequest('user is not logged in')

    # if yes, return the user name and email
    try:
        user = User.objects.get(id=user_id)
        if user is None:
            logger.error(f"[session] user with id {user_id} does not exist")
            return HttpResponseBadRequest('user does not exist')

        if user is not None:
            # Successful login
            logger.info(f"[session] user {user_id} logged in successfully")
            return HttpResponse(
                json.dumps(
                    {
                        'user_name': user.name,
                        'user_email': user.email,
                    }
                ),
                content_type="application/json",
            )

    except Exception as e:
        logger.error(f"[session] failed to get user with id {user_id}: {repr(e)}")
        return HttpResponseBadRequest()
