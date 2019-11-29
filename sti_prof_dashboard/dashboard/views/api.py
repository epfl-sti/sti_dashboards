import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from epfl.sti.helpers import tableau


@login_required
def get_tableau_token(request):
    if request.is_ajax():
        token = tableau.get_Tableau_trusted_authentication_token(settings.TABLEAU_BASE_URL)
        mimetype = 'application/json'
        return HttpResponse(token, mimetype)
