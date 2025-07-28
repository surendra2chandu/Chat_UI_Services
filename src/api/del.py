from azure.identity import DefaultAzureCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder

# Authenticate with Azure
credential = DefaultAzureCredential()
client = GraphServiceClient(credential=credential)

# Get current user's profile
me = client.me.get()
print("=== Current Azure User ===")
print("Display Name:", me.display_name)
print("Email:", me.mail or me.user_principal_name)
print("Job Title:", me.job_title)
print("ID:", me.id)

# Get group memberships
groups = client.me.member_of.get().value
print("\n=== Group Memberships ===")
if not groups:
    print("No groups found.")
else:
    for group in groups:
        display_name = getattr(group, "display_name", None)
        if display_name:
            print("-", display_name)
