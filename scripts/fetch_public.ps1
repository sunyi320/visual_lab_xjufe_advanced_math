param(
    [Parameter(Mandatory=$true)][string]$Manifest
)
$ErrorActionPreference = 'Stop'
$labRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$items = Get-Content -Raw -LiteralPath $Manifest | ConvertFrom-Json
$results = @()
foreach ($item in $items) {
    $destination = [System.IO.Path]::GetFullPath((Join-Path $labRoot $item.path))
    if (-not $destination.StartsWith($labRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Destination outside visual_lab"
    }
    if ([uri]$item.url -and ([uri]$item.url).Scheme -ne 'https') { throw "HTTPS required" }
    New-Item -ItemType Directory -Force -Path ([System.IO.Path]::GetDirectoryName($destination)) | Out-Null
    $record = [ordered]@{url=$item.url; path=$item.path; checked_at=(Get-Date -Format o)}
    try {
        $response = Invoke-WebRequest -Uri $item.url -UseBasicParsing -TimeoutSec 18 -OutFile $destination -PassThru
        $record.status = [int]$response.StatusCode
        $record.bytes = (Get-Item -LiteralPath $destination).Length
        $record.sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $destination).Hash
        $record.ok = $true
    } catch {
        $record.ok = $false
        $record.error = $_.Exception.Message
    }
    $results += [pscustomobject]$record
    Write-Output ($record | ConvertTo-Json -Compress)
}
$logName = [System.IO.Path]::GetFileNameWithoutExtension($Manifest) + '_results.json'
$results | ConvertTo-Json -Depth 8 | Set-Content -Encoding utf8 -LiteralPath (Join-Path $labRoot ('sources/' + $logName))
