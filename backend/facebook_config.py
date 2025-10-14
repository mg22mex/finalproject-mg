# Facebook Configuration
FACEBOOK_APP_ID = "2168203123683107"
FACEBOOK_APP_SECRET = "fa9849c56acdbd7000c89e2fe900d866"

# Facebook Account 1 (Auto Account)
FACEBOOK_ACCOUNTS = [
    {
        "account_name": "Auto Account 1",
        "access_token": "EAAezZBCD87yMBPpmrjUvYzwXDYZCLqgzxOuS8l021ZBHFgmi0EeBLqN6ifTfMlgf1D534UtQ6fdZAGocxZAvclANFVFMpVDoxuyGOEZBE3q5CHB25wEiPHAvg22sISrt3AMQ9GRqFDOyWxWtZCkhtiAdTREIaEhnOZAWq4Yfpzjy0Jew2j7RHiaoxjsxn8depTpNdfOCxZAn9dXeu1qaaWs9BUxCwsRbp7105S2puHVaHzRrfLTnCnPktWQZDZD",
        "page_id": None,  # We'll get this from the API
        "user_id": None,  # We'll get this from the API
        "is_active": True
    }
]

# Facebook API Settings
FACEBOOK_API_VERSION = "v18.0"
FACEBOOK_BASE_URL = f"https://graph.facebook.com/{FACEBOOK_API_VERSION}"

# Posting Settings
DEFAULT_POSTING_SCHEDULE = {
    "enabled": True,
    "frequency_hours": 24,  # Post every 24 hours
    "max_posts_per_day": 3,
    "posting_times": ["09:00", "15:00", "20:00"]  # GMT times
}

# Marketplace Settings
MARKETPLACE_SETTINGS = {
    "enabled": True,
    "auto_repost": True,
    "remove_sold": True,  # Remove from Facebook when marked as "vendido"
    "post_to_page": True,
    "post_to_marketplace": False  # Keep simple for now
}
