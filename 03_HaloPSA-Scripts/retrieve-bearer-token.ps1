# Input bindings for Azure Function (Triggers)
param($Timer)

# Output logs
Write-Output "Azure Function triggered at: $(Get-Date)"

# Variables später als ENV speichern
$authUrl = "https://jokerit.halopsa.com/auth/token"
$clientId = "e6bdb6b7-459f-4bfe-8366-e0affc4ed64b"
$clientSecret = "6083ac28-7fc9-4bca-b9bf-fe9ec83d3df8-5c72a929-b40e-43f7-a35c-43f23fc549ba"
$scope = "all"

# Function to get authentication token
function Get-AuthToken {
    param([string]$grantType = "client_credentials")
    $headers = @{
        "Content-Type" = "application/x-www-form-urlencoded"
    }
    $body = @{
        grant_type    = $grantType
        client_id     = $clientId
        client_secret = $clientSecret
        scope         = $scope
    }
    $response = Invoke-RestMethod -Uri $authUrl -Method Post -Headers $headers -Body $body
    return $response
}

# Retrieve and log the token
$tokenResponse = Get-AuthToken
$bearerToken = $tokenResponse.access_token
$expirationTime = (Get-Date).AddSeconds($tokenResponse.expires_in)
Write-Output "Bearer Token: $bearerToken"
Write-Output "Expires At: $expirationTime"

# You can log the token or store it securely
# Example: Store in Azure Key Vault or write to a database
