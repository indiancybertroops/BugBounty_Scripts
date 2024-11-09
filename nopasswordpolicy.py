# no password policy bug
#++++++++++++++++++++++++++++++++++++++++++++++
# pip install requests beautifulsoup4 lxml (Modules needed)
# install requests, beautifulsoup4, and lxml libraries
# python test_no_password_policy.py (usages)

import requests
from bs4 import BeautifulSoup
import re

# Function to find all URLs on the site
def find_urls(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Check for errors (e.g., 404, 500)
        soup = BeautifulSoup(response.text, 'lxml')
        
        urls = set()  # Use a set to avoid duplicate URLs
        for anchor in soup.find_all('a', href=True):
            url = anchor['href']
            # Handle relative URLs
            if url.startswith('/'):
                url = base_url + url
            elif not url.startswith('http'):
                url = base_url + '/' + url
            urls.add(url)
        
        return list(urls)
    except Exception as e:
        print(f"Error fetching URLs from {base_url}: {e}")
        return []

# Function to test the "No Password Policy Bug"
def test_no_password_policy_signup(base_url):
    # Example of account creation form (this will need to be customized based on the target website)
    signup_url = base_url + "/signup"  # Change this to the actual signup page URL
    test_data = {
        'username': 'testuser123',
        'email': 'testuser123@example.com',
        'password': ''  # Empty password for testing "no password policy"
    }
    
    # Send POST request to create account with no password
    try:
        response = requests.post(signup_url, data=test_data)
        
        if response.status_code == 200:
            # Check if the account creation was successful
            if "account created" in response.text.lower() or "successful" in response.text.lower():
                print(f"BUG: No password policy detected! Able to create account with empty password at {signup_url}")
            else:
                print(f"No bug found in account creation with empty password.")
        else:
            print(f"Error during account creation attempt. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error testing account creation: {e}")

# Main function to execute the script
def main():
    base_url = input("Enter the target website URL (e.g., https://example.com): ").strip()
    
    # 1. Find all URLs on the site
    print("\nFetching all URLs from the site...")
    urls = find_urls(base_url)
    print(f"Found {len(urls)} URLs:")
    for url in urls:
        print(url)
    
    # 2. Test the "No Password Policy Bug" (attempt account creation with empty password)
    print("\nTesting for No Password Policy Bug...")
    test_no_password_policy_signup(base_url)

# Run the script
if __name__ == "__main__":
    main()
