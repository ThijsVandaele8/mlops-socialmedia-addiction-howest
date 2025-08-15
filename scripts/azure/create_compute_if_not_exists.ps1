param (
    [Parameter(Mandatory=$true)]
    [string]$ComputeName
)

$State = & az ml compute show --name $ComputeName --query "state" -o tsv 2>$null

if (-not $State) 
{
    Write-Host "Compute $ComputeName does not exist. Creating..."
    az ml compute create --file ./aml/compute/compute.yaml
} 
else 
{
    Write-Host "Compute $ComputeName exists. State: $State"
}