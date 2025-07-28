import requests
from azure.identity import InteractiveBrowserCredential

# Step 1: Authenticate and get token for Microsoft Graph
credential = InteractiveBrowserCredential()
token = credential.get_token("https://graph.microsoft.com/.default").token

# Step 2: Set headers for Microsoft Graph API call
headers = {
    "Authorization": f"Bearer {token}"
}

# Step 3: Call /me endpoint to get current user info
response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

if response.status_code == 200:
    user = response.json()
    print("=== Current Azure User ===")
    print("Display Name:", user.get("displayName"))
    print("Email:", user.get("mail") or user.get("userPrincipalName"))
    print("Job Title:", user.get("jobTitle"))
    print("User ID:", user.get("id"))
else:
    print("Error:", response.status_code)
    print(response.text)
