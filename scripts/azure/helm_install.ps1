param (
    [Parameter(Mandatory=$true)]
    [string]$namespace,
    [Parameter(Mandatory=$true)]
    [string]$githubsha,    
    [Parameter(Mandatory=$true)]
    [string]$dockerimage
)

$shaShort = $githubsha.Substring(0,7)
$fullDockerImage = "$($dockerimage):sha-$($shaShort)"

helm upgrade --install socialmedia-addiction-regressor .\k8s\socialmedia-addiction `
        --namespace $namespace --create-namespace `
        --set container.image="$fullDockerImage" -f .\k8s\socialmedia-addiction\values.yaml