def set_Hue(url, usr):
    # the base URL
    base_url = 'http://' + url;

    # example username, generated by following https://www.developers.meethue.com/documentation/getting-started
    username = usr

    # lights URL
    lights_url = base_url + '/api/' + username + '/lights/'

    return lights_url


