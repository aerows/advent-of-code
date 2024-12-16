param(
    [Parameter(Mandatory = $false)]
    [string]$SourceFolder = (Join-Path -Path $PSScriptRoot -ChildPath "2024\template"),
    
    [Parameter(Mandatory = $false)]
    [string]$DestinationBaseFolder = (Join-Path -Path $PSScriptRoot -ChildPath "2024"),
    
    [Parameter(Mandatory = $false)]
    [int]$Day
)

# Get current date and format day as two digits, ensuring single digits are padded
Write-Output "SourceFolder: $SourceFolder"
Write-Output "DestinationBaseFolder: $DestinationBaseFolder"
Write-Output "Day: $Day"

$currentDate = Get-Date
$day = if ($Day) {
    [string]([int]$Day).ToString().PadLeft(2, '0')
}
else {
    [string]([int]$currentDate.Day).ToString().PadLeft(2, '0')
}

# Create the destination path with the day folder
$destPath = Join-Path -Path $DestinationBaseFolder -ChildPath $day

# Create the destination directory if it doesn't exist
if (-not (Test-Path -Path $destPath)) {
    New-Item -ItemType Directory -Path $destPath -Force
}

# Copy all contents from source to destination
Get-ChildItem -Path $SourceFolder -Recurse | ForEach-Object {
    $targetPath = $_.FullName.Replace($SourceFolder, $destPath)
    if ($_.PSIsContainer) {
        if (-not (Test-Path -Path $targetPath)) {
            New-Item -ItemType Directory -Path $targetPath -Force
        }
    }
    else {
        Copy-Item -Path $_.FullName -Destination $targetPath -Force
    }
}