import requests
from azure.identity import InteractiveBrowserCredential

# Inputs
subscription_id = "your-subscription-id"  # Replace with actual
resource_group = "DAaaS"

# Step 1: Authenticate to Azure ARM (not Graph!)
credential = InteractiveBrowserCredential()
token = credential.get_token("https://management.azure.com/.default").token

# Step 2: Get current user object ID from Graph
graph_token = credential.get_token("https://graph.microsoft.com/.default").token
graph_headers = {"Authorization": f"Bearer {graph_token}"}
me = requests.get("https://graph.microsoft.com/v1.0/me", headers=graph_headers).json()
user_id = me.get("id")
print("Logged-in User:", me.get("displayName"), "| ID:", user_id)

# Step 3: Query role assignments on the resource group
scope = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
arm_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
url = f"https://management.azure.com{scope}/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01"

response = requests.get(url, headers=arm_headers)
data = response.json()

# Step 4: Filter assignments for current user
print(f"\n=== Role Assignments for user on Resource Group: {resource_group} ===")
found = False
for assignment in data.get("value", []):
    if assignment.get("properties", {}).get("principalId", "").lower() == user_id.lower():
        found = True
        role_id = assignment["properties"]["roleDefinitionId"].split("/")[-1]
        print(f"- Role Assignment ID: {assignment['name']}")
        print(f"  Role ID: {role_id}")
        print(f"  Scope: {assignment['properties']['scope']}")
if not found:
    print("❌ No role assignments found for this user on this resource group.")
