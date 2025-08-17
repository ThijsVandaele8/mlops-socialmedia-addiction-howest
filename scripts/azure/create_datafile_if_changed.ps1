param(
    [Parameter(Mandatory=$true)]
    [string]$contentPath,
    [Parameter(Mandatory=$true)]
    [string]$dataYamlPath,
    [Parameter(Mandatory=$true)]
    [string]$dataName
)

. "$PSScriptRoot\..\utils.ps1"

$fullContentPath = (Resolve-Path $contentPath).Path
Write-Host "Full content path: $fullContentPath"

$dataInfo = Test-CloudFileHash -contentPath $fullContentPath -dataName $dataName

if (-not $dataInfo.IsSame)
{
    $dataYamlContent = Get-Content $dataYamlPath
    $dataYamlContent = $dataYamlContent -replace "{{hash}}", $dataInfo.LocalHash -replace "{{path}}", $fullContentPath

    $tempYamlPath = "$env:TEMP\socialmedia_data_temp.yaml"
    $dataYamlContent | Set-Content -Path $tempYamlPath -Encoding UTF8

    $version = az ml data create --file $tempYamlPath --query "version"
}

$displayVersion = if ($dataInfo.IsSame) { $dataInfo.CloudVersion } else { $version }
Write-Host "Latest version: $displayVersion"