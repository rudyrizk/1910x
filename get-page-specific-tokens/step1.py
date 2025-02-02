import requests
from requests_oauthlib import OAuth1

# Your API credentials from X DEV ACCOUNT - SAME FOR ALL - FIRST 2 KEYS (API Key and Secret )
consumer_key = '....dQX'
consumer_secret = ''

# Define the URL for requesting the OAuth token
request_token_url = 'https://api.twitter.com/oauth/request_token'

# Initialize OAuth1 object for signing the request
auth = OAuth1(consumer_key, consumer_secret)

# Send the request to get the request token
response = requests.post(request_token_url, auth=auth)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response
    credentials = dict(x.split('=') for x in response.text.split('&'))

    # Extract the oauth_token and oauth_token_secret
    oauth_token = credentials.get('oauth_token')
    oauth_token_secret = credentials.get('oauth_token_secret')

    print("OAuth Token:", oauth_token)
    print("OAuth Token Secret:", oauth_token_secret)

    # You will need to use this oauth_token in the next steps to authorize the user
    print("\nThe user must now authorize the app.")
    print(f"Go to the following URL to authorize:")
    print(f"https://api.twitter.com/oauth/authorize?oauth_token={oauth_token}")

else:
    print("Failed to obtain request token. Status code:", response.status_code)
    print("Response:", response.text)
