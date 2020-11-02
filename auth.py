def get_user(request):

    login_value = request.get_argument('username')
    password = request.get_argument('password')

    if (login_value == 'nyc') and (password == 'iheartnyc'):
        return 1
    else:
        return None

login_url = '/login'
