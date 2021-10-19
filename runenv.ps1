# premade activation script activator, ready for usage
# Free to use and modify
# Made by MXPSQL



# parameters
Param(
    [Parameter(Mandatory = $false)]
    [String]
    $VenvDir = (Get-Location | Out-String),
    [Parameter(Mandatory = $false)]
    [String]
    $Prompt = "pwsh-venv"
)

# activate the enviorment
./env/Scripts/Activate.ps1 -Prompt $Prompt -VenvDir "$VenvDir"