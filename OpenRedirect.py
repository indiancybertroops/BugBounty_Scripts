# Testing Open Redirect Vulnerability
# pip install requests argparse (Modules needed)
# python open_redirect_test.py https://example.com/register --redirect https://www.google.com (usages)
import requests
import argparse
from urllib.parse import urlparse, urlencode, urlunparse


# Function to test Open Redirect vulnerability
def test_open_redirect(target_url, redirect_uri):
    """
    Test if a given target URL has an open redirect vulnerability by modifying the redirect_uri.
    
    :param target_url: The URL of the registration or login page with the redirect-uri parameter.
    :param redirect_uri: The redirect URI value (e.g., "https://www.google.com").
    :return: None
    """
    print(f"Testing Open Redirect with target: {target_url}")
    
    # Parse the target URL and modify the redirect_uri parameter
    parsed_url = urlparse(target_url)
    
    # Check if the URL contains the redirect-uri parameter
    if "redirect-uri=" in parsed_url.query:
        # Modify the redirect-uri parameter to test for open redirect
        query_params = dict(parse_qsl(parsed_url.query))
        query_params["redirect-uri"] = redirect_uri  # Change this value to test different URIs

        # Rebuild the URL with the modified query string
        modified_url = parsed_url._replace(query=urlencode(query_params)).geturl()

        # Send a request with the modified URL
        try:
            response = requests.get(modified_url, allow_redirects=False)  # Disable automatic redirects
            if response.status_code == 200:
                print(f"[*] Open Redirect detected: {modified_url}")
            else:
                print(f"[-] No redirect detected for: {modified_url}")
        except requests.exceptions.RequestException as e:
            print(f"[!] Error while testing Open Redirect: {e}")
    else:
        print("[!] No redirect-uri parameter found in the URL!")


# Function to parse arguments from the command line
def parse_args():
    parser = argparse.ArgumentParser(description="Test Open Redirect vulnerability")
    parser.add_argument("url", help="The target URL of the page with redirect-uri parameter (e.g., https://example.com/register)")
    parser.add_argument("--redirect", default="https://www.google.com", help="Redirect URI to test (default is https://www.google.com)")
    return parser.parse_args()


# Main function to run the script
def main():
    args = parse_args()

    target_url = args.url
    redirect_uri = args.redirect

    # Test for Open Redirect vulnerability
    test_open_redirect(target_url, redirect_uri)


# Run the script
if __name__ == "__main__":
    main()
