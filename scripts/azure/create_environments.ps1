param (
    [Parameter(Mandatory=$true)]
    [string]$socialmedia_SourceCode_Uri
)
Write-Host "SourceCode_Uri $socialmedia_SourceCode_Uri"
$condaFiles = Get-ChildItem -Path ".\aml\environments" -File |
    Where-Object { $_.Name -like '*conda.yaml' } 

foreach($condaFile in $condaFiles)
{
    (Get-Content $condaFile).Replace('{socialmedia-sourcecode-uri}', $socialmedia_SourceCode_Uri) | Set-Content $condaFile
}

$environments = Get-ChildItem -Path ".\aml\environments" -File |
    Where-Object { $_.Name -notlike '*conda.yaml' } 

foreach($environment in $environments)
{
    Write-Host "Create environment $environment"
    az ml environment create --file $environment.FullName
}