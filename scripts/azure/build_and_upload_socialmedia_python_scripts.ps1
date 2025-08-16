param (
    [Parameter(Mandatory=$true)]
    [string]$workspaceName,
    [Parameter(Mandatory=$true)]
    [string]$resourceGroup
)

python setup.py bdist_wheel

$path = az ml data create --file './aml/data/bin/modeling.yaml' --query "path" --output tsv
$blobName = $path -replace ".*?/paths/", ""

$datastoreInfo = az ml datastore show `
    --name workspaceblobstore `
    --workspace-name $workspaceName `
    --resource-group $resourceGroup `
    --query "{account:account_name, container:container_name}" `
    -o json | ConvertFrom-Json

$expiry = (Get-Date).ToUniversalTime().AddHours(1).ToString("yyyy-MM-ddTHH:mm:ssZ")

$sasToken = az storage blob generate-sas `
    --account-name $datastoreInfo.account `
    --container-name $datastoreInfo.container `
    --name $blobName `
    --permissions r `
    --expiry $expiry `
    --https-only `
    --output tsv

$blobUrl = "https://$($datastoreInfo.account).blob.core.windows.net/$($datastoreInfo.container)/$blobName"
$uriWithSas = "$blobUrl`?$sasToken"

Write-Output $uriWithSas
