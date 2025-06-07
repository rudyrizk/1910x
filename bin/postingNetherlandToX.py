import requests
import tweepy
import re
import os
from datetime import datetime

API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN_NL')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET_NL')
# BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# # Set up Twitter API authentication
# auth = tweepy.OAuth1UserHandler(
#     consumer_key=API_KEY,
#     consumer_secret=API_SECRET_KEY,
#     access_token=ACCESS_TOKEN,
#     access_token_secret=ACCESS_TOKEN_SECRET
# )
# api = tweepy.API(auth)

# # Initialize the Tweepy client with your Bearer Token
# client = tweepy.Client(bearer_token=BEARER_TOKEN,
#                        consumer_key=API_KEY,
#                        consumer_secret=API_SECRET_KEY,
#                        access_token=ACCESS_TOKEN,
#                        access_token_secret=ACCESS_TOKEN_SECRET)

# Initialize Tweepy Client for v2 (do NOT include bearer_token for posting)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Function to fetch content from a URL
def fetch_content(url):
    # Send GET request to the URL
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Get the response text
        content = response.text
        
        # Remove everything after "Bron : Petrus Canisius bijbelvertaling"
        cleaned_content = re.sub(r'<br\s*/?>', '', content)
        cleaned_content = re.sub(r'&quot;', '', cleaned_content)
        cleaned_content = re.sub(r'&#039;', "'", cleaned_content)
        cleaned_content = re.split(r'Bron : Petrus Canisius bijbelvertaling', cleaned_content)[0]

        # Parse the HTML to remove all HTML tags
        #soup = BeautifulSoup(cleaned_content, 'html.parser')
        #cleaned_content = soup.get_text()  # Extract just the text
        
        return cleaned_content
    else:
        print(f"Failed to retrieve content from {url}.")
        return None

# Function to get today's dynamic date
def get_today_date():
    return datetime.now().strftime('%Y%m%d')

# Function to get the dynamically formatted date for the final URL
def get_formatted_date():
    return datetime.now().strftime('%Y-%m-%d')

# Function to combine the contents and return the final result
def get_combined_content():
    # Get today's dynamic date
    today = get_today_date()

    # URLs for fetching content
    url1 = f"https://feed.evangelizo.org/v2/reader.php?lang=NL&type=reading&content=GSP&date={today}"
    url2 = f"https://feed.evangelizo.org/v2/reader.php?date={today}&lang=NL&type=liturgic_t&content=GSP"

    # Fetch and clean the content from both URLs
    content1 = fetch_content(url1)
    content2 = fetch_content(url2)

    if content1 and content2:
        # Add a break line between the two contents
        final_content = content1 + "\n\n" + content2
        
        # Add the final URL at the end with the formatted date
        formatted_date = get_formatted_date()
        final_content += f"\nGa verder met alle lezingen van vandaag https://dagelijksevangelie.org/NL/gospel/{formatted_date}" + "\n" +"\n" + '#dagelijksevangelie #jezus #evangelie'
        #print(final_content)
        return final_content
    else:
        print("Failed to retrieve or clean content.")
        return None

# Function to post content to Twitter
def post_to_twitter(content):
    if content:
        try:
            # Post the content to Twitter using API v2 (Tweepy v4.x)
            # client.create_tweet(text=content)
            # print("Successfully posted to Twitter!")
            response = client.create_tweet(text=content)
            print("Successfully posted:", response)
        except Exception as e:
            print("Failed to post:", e)
        # except tweepy.TweepError as e:
        #     print(f"Error posting to Twitter: {e}")
    else:
        print("No content to post.")

# Function to post content to Twitter
def post_to_twitter_OLD(content):
    if content:
        try:
            # Post the content to Twitter
            api.update_status(content)
            print("Successfully posted to Twitter!")
        except tweepy.TweepError as e:
            print(f"Error posting to Twitter: {e}")
    else:
        print("No content to post.")


if __name__ == "__main__":
    #post_to_twitter("alingilalyawmi.org")
    # Example usage:
    final_content = get_combined_content()
    if final_content:
        print(final_content)  # Print the final combined content
        # Post the fetched content to Twitter
        post_to_twitter(final_content)
