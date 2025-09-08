"""
Facebook Configuration Example
Copy this file to facebook_config.py and fill in your actual values
"""

# Facebook API Configuration
FACEBOOK_CONFIG = {
    # Get this from Facebook Developer Console
    "APP_ID": "your_facebook_app_id_here",
    "APP_SECRET": "your_facebook_app_secret_here",
    
    # User Access Token (for Marketplace posting)
    "USER_ACCESS_TOKEN": "your_user_access_token_here",
    "USER_ID": "your_facebook_user_id_here",
    
    # Page Access Token (for posting to Facebook page)
    "PAGE_ACCESS_TOKEN": "your_page_access_token_here",
    "PAGE_ID": "your_facebook_page_id_here",
}

# How to get these credentials:
#
# 1. APP_ID & APP_SECRET:
#    - Go to https://developers.facebook.com/
#    - Create a new app or use existing one
#    - Go to Settings > Basic
#    - Copy App ID and App Secret
#
# 2. USER_ACCESS_TOKEN:
#    - Go to https://developers.facebook.com/tools/explorer/
#    - Select your app
#    - Click "Generate Access Token"
#    - Grant necessary permissions (pages_manage_posts, marketplace_manage_listings)
#    - Copy the access token
#
# 3. PAGE_ACCESS_TOKEN:
#    - Use the Graph API Explorer
#    - Make a GET request to: /{page_id}?fields=access_token
#    - Use the user access token with page permissions
#    - Copy the page access token
#
# 4. PAGE_ID:
#    - Go to your Facebook page
#    - Look at the URL: facebook.com/YourPageName
#    - Or use the page ID from page settings
#
# 5. USER_ID:
#    - Use the Graph API Explorer
#    - Make a GET request to: /me
#    - Copy the "id" field
#
# Required Permissions:
# - pages_manage_posts (for posting to page)
# - marketplace_manage_listings (for marketplace)
# - pages_read_engagement (for reading page data)
