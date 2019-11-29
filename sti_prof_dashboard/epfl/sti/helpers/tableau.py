import requests

def get_Tableau_trusted_authentication_token(tableau_base_url):
    payload = {
        'username': 'intranet\sti_dashboard_viewer'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    r = requests.post(tableau_base_url, params=payload)
    response = r.text

    return response
