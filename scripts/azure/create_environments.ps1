$environments = Get-ChildItem -Path ".\aml\environments" -File |
    Where-Object { $_.Name -notlike '*conda.yaml' } 

foreach($environment in $environments)
{
    Write-Host "Create environment $environment"
    az ml environment create --file $environment.FullName
}