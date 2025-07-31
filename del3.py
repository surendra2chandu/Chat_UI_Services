# Importing necessary libraries
import requests
from azure.identity import AzureAuthorityHosts, DefaultAzureCredential
from src.conf.Configurations import logger, GROUP_INFO, ALLOWED_CATEGORIES


class UserIdentityProvider:
    def __init__(self):
        """
        Initializes the UserIdentityProvider to handle user identity retrieval and RBAC role definitions
        """
        # Create the credential using the Azure Government authority host
        logger.info("Initializing UserIdentityProvider for Azure Government Cloud")
        self.credential = DefaultAzureCredential(
            authority=AzureAuthorityHosts.AZURE_GOVERNMENT
        )

    def get_user_identity(self):
        """
        Retrieves the current user's identity and role definitions in Azure Government Cloud.
        """
        # This method can be expanded to return user identity details if needed
        # To Get token for Graph in US Gov Cloud
        logger.info("getting tokens for  Graph in Azure Government Cloud")
        graph_token = self.credential.get_token("https://graph.microsoft.us/.default").token
        logger.info(f"graph_token: {graph_token}")

        # Get current user object ID from Microsoft Graph (US Gov)
        logger.info("Retrieving current user object ID from Microsoft Graph")
        graph_headers = {"Authorization": f"Bearer {graph_token}"}
        user_details_resp = requests.get("https://graph.microsoft.us/v1.0/me", headers=graph_headers)
        user_details = user_details_resp.json()
        logger.info(f"user_details: {user_details}")
        user_name = user_details.get("displayName", "System")
        user_id = user_details.get("id")
        logger.info(f"Logged-in User: {user_details.get('displayName')}, Object ID: {user_id}")

        # Getting user groups with specific fields
        group_url = f"https://graph.microsoft.us/v1.0/users/{user_id}/memberOf?$select=displayName,id,description"

        group_response = requests.get(group_url, headers=graph_headers)
        allowed_values = []

        if group_response.status_code == 200:
            groups = group_response.json().get("value", [])
            logger.info(f"groups: {groups}")

            # Retrieve all group names
            group_names = [group.get("displayName", "Unknown Group") for group in groups]
            logger.info(f"group_names: {group_names}")

            for key, value in GROUP_INFO.items():

                for group in value:
                    if group in group_names:
                        allowed_values.append(key)
                        logger.info(f"User {user_name} is part of group: {group}, allowing category: {key}")

            allowed_values.extend(ALLOWED_CATEGORIES) # Always allow DAaaS Admin
        else:
            logger.error(f"Failed to retrieve user groups: {group_response.status_code} - {group_response.text}")
            allowed_values = ALLOWED_CATEGORIES

        return user_name, allowed_values



# Example usage
if __name__ == "__main__":
    provider = UserIdentityProvider()
    res = provider.get_user_identity()
    print(res)

