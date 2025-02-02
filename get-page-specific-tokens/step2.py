import requests
from requests_oauthlib import OAuth1

# Your API credentials and tokens from previous step
consumer_key = ''
consumer_secret = ''
oauth_token = ''  # oauth_token from previous step
oauth_token_secret = ''  # oauth_token_secret from previous step
oauth_verifier = ''  # oauth_verifier after user authorizes your app

# Define the URL for accessing the access token
access_token_url = 'https://api.twitter.com/oauth/access_token'

# Initialize OAuth1 object for signing the request
auth = OAuth1(consumer_key, consumer_secret, oauth_token, oauth_token_secret)

# Send the request to exchange the request token for an access token
response = requests.post(access_token_url, auth=auth, data={'oauth_verifier': oauth_verifier})

# Check if the request was successful
if response.status_code == 200:
    # Parse the response to extract the access token and secret
    credentials = dict(x.split('=') for x in response.text.split('&'))

    # Extract the oauth_token (access token) and oauth_token_secret
    access_token = credentials.get('oauth_token')
    access_token_secret = credentials.get('oauth_token_secret')

    print("Access Token:", access_token)
    print("Access Token Secret:", access_token_secret)

    # Now you have the access token and access token secret that you can use for future authenticated requests
else:
    print("Failed to obtain access token. Status code:", response.status_code)
    print("Response:", response.text)
