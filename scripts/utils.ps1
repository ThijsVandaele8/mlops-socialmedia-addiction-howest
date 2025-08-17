function Test-CloudFileHash
{
    param(
        [Parameter(Mandatory)]
        [string]$contentPath,
        [Parameter(Mandatory=$true)]
        [string]$dataName
    )

    $hashLocal = Get-PathHash -Path $contentPath
    Write-Host "Local hash: $hashLocal"

    $latestVersion = az ml data list --query "[?name=='$dataName'] | [0].latest_version" -o tsv
    $hashCloud = az ml data show --name "$dataName" --version $latestVersion --query "tags.hash" -o tsv
    Write-Host "Cloud hash: $hashCloud"

    $isSame = ($hashCloud -and $hashCloud -eq $hashLocal)
    if ($isSame)
    {
        Write-Host "dataname $($dataName) is not changed"
    }
    else
    {
        Write-Host "dataname $($dataName) is changed"
    }

    return [PSCustomObject]@{
        IsSame    = $isSame
        LocalHash = $hashLocal
        CloudHash = $hashCloud
        CloudVersion = $latestVersion
    }
}

function Get-PathHash 
{
    param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    if (-not (Test-Path $Path)) 
    {
        throw "Path does not exist: $Path"
    }

    if (Test-Path $Path -PathType Leaf) 
    {
        return (Get-FileHash -Path $Path -Algorithm SHA256).Hash
    }

    elseif (Test-Path $Path -PathType Container) 
    {
        $files = Get-ChildItem -Path $Path -File -Recurse | Sort-Object FullName
        $hasher = [System.Security.Cryptography.HashAlgorithm]::Create("SHA256")

        foreach ($file in $files) 
        {
            $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
            $hasher.TransformBlock($bytes, 0, $bytes.Length, $bytes, 0) | Out-Null
        }

        $hasher.TransformFinalBlock(@(), 0, 0) | Out-Null
        return ([BitConverter]::ToString($hasher.Hash)).Replace("-", "")
    }
    else 
    {
        throw "Unknown path type: $Path"
    }
}
