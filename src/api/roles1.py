import requests
from azure.identity import InteractiveBrowserCredential

# Step 1: Authenticate and get a token
credential = InteractiveBrowserCredential()
token = credential.get_token("https://graph.microsoft.com/.default").token

# Step 2: Set up headers for Microsoft Graph API
headers = {
    "Authorization": f"Bearer {token}"
}

# Step 3: Get current user details
user_response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
if user_response.status_code == 200:
    user = user_response.json()
    print("=== Current Azure User ===")
    print("Display Name:", user.get("displayName"))
    print("Email:", user.get("mail") or user.get("userPrincipalName"))
    print("Job Title:", user.get("jobTitle"))
    print("User ID:", user.get("id"))
else:
    print("Error fetching user info:", user_response.status_code)
    exit()

# Step 4: Get group memberships (roles)
group_response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf", headers=headers)
if group_response.status_code == 200:
    groups = group_response.json().get("value", [])
    print("\n=== Group Memberships / Roles ===")
    if not groups:
        print("No groups found.")
    else:
        for group in groups:
            name = group.get("displayName") or group.get("id")
            type_ = group.get("@odata.type", "").split(".")[-1]
            print(f"- {name} ({type_})")
else:
    print("Error fetching groups:", group_response.status_code)
    print(group_response.text)
