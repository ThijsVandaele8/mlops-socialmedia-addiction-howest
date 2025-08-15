param (
    [Parameter(Mandatory=$true)]
    [string]$ComputeName
)

$STATE=$(az ml compute show --name $ComputeName --query "state" -o tsv)

if($STATE -ne "Running")
{
    Write-Host "Compute is not running"
    az ml compute start --name $ComputeName
}

Write-Host "Compute is running"