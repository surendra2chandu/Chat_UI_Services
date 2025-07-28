from azure.identity import DefaultAzureCredential
from msgraph.core import GraphClient

# Step 1: Authenticate with Azure
credential = DefaultAzureCredential()
client = GraphClient(credential=credential)

# Step 2: Get current user details
user_response = client.get('/me')
user = user_response.json()

print("=== Current Azure User ===")
print("Display Name:", user.get("displayName"))
print("Email:", user.get("mail") or user.get("userPrincipalName"))
print("Job Title:", user.get("jobTitle"))
print("ID:", user.get("id"))

# Step 3: Get user group memberships (roles)
groups_response = client.get('/me/memberOf')
groups = groups_response.json().get("value", [])

print("\n=== Group Memberships ===")
if not groups:
    print("No groups found.")
else:
    for group in groups:
        print("-", group.get("displayName"))
