from azure.identity import DefaultAzureCredential
from msgraph.core import GraphClient

# Authenticate with Azure CLI or environment
credential = DefaultAzureCredential()
client = GraphClient(credential=credential)

# Get current user details
me_response = client.get('/me')
me = me_response.json()

print("=== Current Azure User ===")
print("Name:", me.get("displayName"))
print("Email:", me.get("mail") or me.get("userPrincipalName"))
print("Job Title:", me.get("jobTitle"))
print("ID:", me.get("id"))

# Get user group memberships
group_response = client.get('/me/memberOf')
groups = group_response.json().get("value", [])

print("\n=== Group Memberships ===")
if not groups:
    print("No groups found.")
else:
    for group in groups:
        name = group.get("displayName")
        if name:
            print("-", name)
