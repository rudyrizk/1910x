import requests
import tweepy
import re
import os
from datetime import datetime
import traceback
import time

API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# Set up Twitter API authentication
auth = tweepy.OAuth1UserHandler(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

# Initialize the Tweepy client with your Bearer Token
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY,
                       consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)


# Function to fetch content from the URL
def fetch_content():
    # Get today's date in the format YYYYMMDD
    today = datetime.now().strftime('%Y%m%d')
    
    # URL for fetching content
    url = f"https://feed.evangelizo.org/v2/reader.php?lang=MAA&type=reading&content=GSP&date={today}"

    # Send GET request to the URL
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        # Get the response text
        content = response.text
        
        # Use regular expression to remove everything starting from "النصوص مأخوذة من الترجمة" onward
        #cleaned_content = re.sub(r'<br />*', '', content)
        # Remove all <br />, <br> or <br/> tags
        cleaned_content = re.sub(r'<br\s*/?>', '', content)

        cleaned_content = re.split(r'النصوص مأخوذة من الترجمة', cleaned_content)[0]

        # Return the cleaned content (everything before the specified text)
        return cleaned_content
    else:
        print("Failed to retrieve content.")
        return None

# Function to fetch content from a URL
def fetch_content(url):
    # Send GET request to the URL
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=15)
    response_code = response.status_code
    
    # Check if request was successful
    if response.status_code == 200:
        # Get the response text
        content = response.text
        
        # Remove everything after "النصوص مأخوذة من الترجمة"
        #cleaned_content = re.split(r'النصوص مأخوذة من الترجمة', content)[0]
        cleaned_content = re.sub(r'<br\s*/?>', '', content)
        cleaned_content = re.split(r'النصوص مأخوذة من الترجمة', cleaned_content)[0]

        # Parse the HTML to remove all HTML tags
        #soup = BeautifulSoup(cleaned_content, 'html.parser')
        #cleaned_content = soup.get_text()  # Extract just the text
        
        return cleaned_content
    else:
        print(f"Failed to retrieve content from {url}.")
        print(f"Response status code {response_code}.")
        
        return None

def fetch_content_extensive_logs(url):
    print("=" * 80)
    print(f"[INFO] Starting fetch_content()")
    print(f"[INFO] URL: {url}")
    # print(f"[INFO] Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    start_time = time.time()

    try:
        print("[DEBUG] Sending GET request...")
        response = requests.get(url, timeout=15)

        duration = round(time.time() - start_time, 3)

        print("[INFO] Request completed")
        print(f"[INFO] Status Code: {response.status_code}")
        print(f"[INFO] Duration: {duration}s")

        print("[DEBUG] Response Headers:")
        for k, v in response.headers.items():
            print(f"    {k}: {v}")

        print(f"[DEBUG] Content-Length header: {response.headers.get('Content-Length')}")
        print(f"[DEBUG] Encoding: {response.encoding}")
        print(f"[DEBUG] Apparent Encoding: {response.apparent_encoding}")

        print(f"[DEBUG] Raw content length: {len(response.content)} bytes")

        # Try JSON safely
        try:
            json_data = response.json()
            print("[DEBUG] JSON detected in response:")
            print(json_data)
        except Exception as json_error:
            print("[DEBUG] Response is not valid JSON")
            print(f"[DEBUG] JSON parsing error: {json_error}")

        # Log preview of body (first 500 chars only)
        preview = response.text[:500]
        print("[DEBUG] Response preview (first 500 chars):")
        print(preview)

        # If success
        if response.status_code == 200:
            print("[INFO] Status 200 OK — processing content")

            content = response.text

            print("[DEBUG] Removing <br> tags...")
            cleaned_content = re.sub(r'<br\s*/?>', '', content)

            print("[DEBUG] Splitting on Arabic marker...")
            cleaned_content = re.split(
                r'النصوص مأخوذة من الترجمة',
                cleaned_content
            )[0]

            print(f"[INFO] Cleaned content length: {len(cleaned_content)} chars")

            return cleaned_content

        else:
            print("[ERROR] Non-200 response received")
            print(f"[ERROR] URL: {url}")
            print(f"[ERROR] Status Code: {response.status_code}")
            print(f"[ERROR] Reason: {response.reason}")
            print(f"[ERROR] Response Text: {response.text}")
            print(f"[ERROR] Raw Bytes: {response.content}")

            return None

    except requests.exceptions.Timeout:
        print("[CRITICAL] Request timed out")
        return None

    except requests.exceptions.ConnectionError as e:
        print("[CRITICAL] Connection error occurred")
        print(f"[CRITICAL] Details: {e}")
        return None

    except requests.exceptions.RequestException as e:
        print("[CRITICAL] General request exception occurred")
        print(f"[CRITICAL] Details: {e}")
        return None

    except Exception as e:
        print("[FATAL] Unexpected error occurred")
        print(f"[FATAL] Error: {e}")
        print("[FATAL] Traceback:")
        traceback.print_exc()
        return None

    finally:
        total_duration = round(time.time() - start_time, 3)
        print(f"[INFO] fetch_content() finished in {total_duration}s")
        print("=" * 80)
        
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
    url1 = f"https://feed.evangelizo.org/v2/reader.php?lang=MAA&type=reading&content=GSP&date={today}"
    url2 = f"https://feed.evangelizo.org/v2/reader.php?date={today}&lang=MAA&type=liturgic_t&content=GSP"

    # Fetch and clean the content from both URLs
    content1 = fetch_content(url1)
    content2 = fetch_content(url2)

    if content1 and content2:
        # Add a break line between the two contents
        final_content = content1 + "\n\n" + content2
        
        # Add the final URL at the end with the formatted date
        formatted_date = get_formatted_date()
        final_content += f"\nلمتابعة كافة قراءات اليوم https://alingilalyawmi.org/MAA/gospel/{formatted_date}" + "\n" + '#إنجيل #الله #يسوع '
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
            client.create_tweet(text=content)
            print("Successfully posted to Twitter!")
        except tweepy.TweepError as e:
            print(f"Error posting to Twitter: {e}")
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

