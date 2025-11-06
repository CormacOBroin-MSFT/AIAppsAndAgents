# GitHub Actions Setup Instructions

This repository includes a GitHub Actions workflow that automatically builds and deploys the application to Azure Container Registry when code is pushed to the `main` branch.

## Required GitHub Secrets

To make the CI/CD pipeline work, you need to set up the following secrets in your GitHub repository:

### 1. AZURE_CREDENTIALS
Create an Azure Service Principal and add it as a JSON secret:

```bash
# Create a service principal
az ad sp create-for-rbac --name "github-actions-sp" --role contributor --scopes /subscriptions/YOUR_SUBSCRIPTION_ID --sdk-auth
```

The output should look like this - add this entire JSON as the `AZURE_CREDENTIALS` secret:
```json
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "...",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

### 2. ACR_LOGIN_SERVER
Your Azure Container Registry login server URL:
```
guemrbcm4kyq6cosureg.azurecr.io
```

### 3. ACR_USERNAME
For admin access, use:
```
guemrbcm4kyq6cosureg
```

### 4. ACR_PASSWORD
Get the admin password from Azure portal or CLI:
```bash
az acr credential show --name guemrbcm4kyq6cosureg --query "passwords[0].value" -o tsv
```

### 5. ENV
Your complete .env file content as a single secret. This should include all environment variables like:

```env
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_KEY=...
SEARCH_ENDPOINT=...
SEARCH_KEY=...
# ... all other environment variables
```

## How to Set GitHub Secrets

1. Go to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Add each secret with the exact name and value

## Workflow Features

- **Triggers**: Automatically runs on push to `main` branch
- **Context**: Builds from the `src/` directory
- **Security**: 
  - `.env` file is created at build time from GitHub secrets
  - `.env` is never committed to the repository
  - `.env` is cleaned up after build
- **Output**: Pushes Docker image to ACR with tag `aiappsandagents:latest`

## Manual Testing

You can also manually trigger the workflow:
1. Go to the "Actions" tab in your GitHub repository
2. Select "Deploy to Azure Container Registry"
3. Click "Run workflow"

## Troubleshooting

- **Authentication errors**: Verify your Azure credentials and ACR passwords
- **Build errors**: Check that all required environment variables are in the `ENV` secret
- **Permission errors**: Ensure the service principal has contributor access to your subscription and ACR