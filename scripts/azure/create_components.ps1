$components = Get-ChildItem -Path ".\aml\components" -File -Recurse |
              Select-Object -ExpandProperty FullName

foreach($component in $components)
{
    Write-Host "Create component $component"
    az ml component create --file $component
}