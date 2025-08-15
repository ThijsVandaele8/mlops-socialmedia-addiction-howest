$version = az ml model list -n socialmedia-addication --query "[0].version" -o tsv
az ml model download -n socialmedia-addication -v $version --download-path models/