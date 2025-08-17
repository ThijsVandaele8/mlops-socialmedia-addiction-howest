param (
    [Parameter(Mandatory=$true)]
    [string]$contentPath,
    [Parameter(Mandatory=$true)]
    [string]$dataYamlPath,
    [Parameter(Mandatory=$true)]
    [string]$dataName,
    [Parameter(Mandatory=$true)]
    [string]$workspaceName,
    [Parameter(Mandatory=$true)]
    [string]$resourceGroup
)
# Build
python setup.py bdist_wheel

# Compare
. "$PSScriptRoot\..\utils.ps1"

$fullContentPath = (Resolve-Path $contentPath).Path
Write-Host "Full content path: $fullContentPath"

$dataInfo = Test-CloudFileHash -contentPath $fullContentPath -dataName $dataName

if (-not $dataInfo.IsSame)
{
    $dataYamlContent = Get-Content $dataYamlPath
    $dataYamlContent = $dataYamlContent -replace "{{hash}}", $dataInfo.LocalHash -replace "{{path}}", $fullContentPath

    $tempYamlPath = "$env:TEMP\$dataName.yaml"
    $dataYamlContent | Set-Content -Path $tempYamlPath -Encoding UTF8

    $blobPath = az ml data create --file $tempYamlPath --query "path" --output tsv
}
else 
{
    $blobPath = az ml data show --name $dataName --version $dataInfo.CloudVersion --workspace-name $workspaceName --resource-group $resourceGroup --query "path" --output tsv
}

$displayVersion = if ($dataInfo.IsSame) { $dataInfo.CloudVersion } else { $version }
Write-Host "Latest version: $displayVersion"

# Generate Sas
$blobName = $blobPath -replace ".*?/paths/", ""

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

"socialmedia_sourcecode_uri=$uriWithSas" | Out-File -FilePath $env:GITHUB_OUTPUT -Encoding utf8 -Append

