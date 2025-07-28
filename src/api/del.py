from azure.identity import DefaultAzureCredential
import requests

def get_current_user_info_and_roles():
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()
    scope = "https://graph.microsoft.com/.default"
    access_token = credential.get_token(scope).token

    # Set request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Step 1: Get current user details
    me_url = "https://graph.microsoft.com/v1.0/me"
    me_response = requests.get(me_url, headers=headers)
    if me_response.status_code != 200:
        print("Failed to fetch user info:", me_response.text)
        return
    me_data = me_response.json()

    print("🔹 User Name:", me_data.get("displayName"))
    print("🔹 User Principal Name:", me_data.get("userPrincipalName"))

    # Step 2: Get current user roles (directory roles)
    roles_url = "https://graph.microsoft.com/v1.0/me/memberOf"
    roles_response = requests.get(roles_url, headers=headers)
    if roles_response.status_code != 200:
        print("Failed to fetch roles:", roles_response.text)
        return
    roles_data = roles_response.json()

    print("\n🔸 Assigned Azure AD Roles:")
    roles = roles_data.get("value", [])
    if not roles:
        print("No roles assigned.")
    else:
        for role in roles:
            role_name = role.get("displayName")
            if role_name:
                print("-", role_name)

if __name__ == "__main__":
    get_current_user_info_and_roles()
