import requests
from azure.identity import InteractiveBrowserCredential, AzureAuthorityHosts

# Step 1: Use the Gov Cloud authority host
credential = InteractiveBrowserCredential(
    authority=AzureAuthorityHosts.AZURE_GOVERNMENT
)

# Step 2: Get token for ARM and Graph in US Gov Cloud
arm_token = credential.get_token("https://management.usgovcloudapi.net/.default").token
graph_token = credential.get_token("https://graph.microsoft.us/.default").token

# Step 3: Get current user object ID from Microsoft Graph (US Gov)
graph_headers = {"Authorization": f"Bearer {graph_token}"}
me_response = requests.get("https://graph.microsoft.us/v1.0/me", headers=graph_headers)
user = me_response.json()
user_id = user.get("id")
print("Logged-in User:", user.get("displayName"))
print("Object ID:", user_id)

# Inputs for RBAC lookup
subscription_id = "your-subscription-id"  # Replace
resource_group = "DAaaS"
scope = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"

# Step 4: Get role assignments from ARM (US Gov)
role_assignments_url = f"https://management.usgovcloudapi.net{scope}/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01"
arm_headers = {
    "Authorization": f"Bearer {arm_token}",
    "Content-Type": "application/json"
}
response = requests.get(role_assignments_url, headers=arm_headers)
assignments = response.json().get("value", [])

# Step 5: Resolve roleDefinitionId to role names
print(f"\n=== RBAC Roles on Resource Group: {resource_group} ===")
for assignment in assignments:
    props = assignment.get("properties", {})
    if props.get("principalId", "").lower() == user_id.lower():
        role_def_id = props.get("roleDefinitionId").split("/")[-1]
        role_def_url = f"https://management.usgovcloudapi.net{scope}/providers/Microsoft.Authorization/roleDefinitions/{role_def_id}?api-version=2022-04-01"
        role_def_resp = requests.get(role_def_url, headers=arm_headers)
        if role_def_resp.status_code == 200:
            role_name = role_def_resp.json()["properties"]["roleName"]
            print(f"- {role_name} (Role ID: {role_def_id})")
        else:
            print(f"- Unknown role ID: {role_def_id}")
