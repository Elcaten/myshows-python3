<#
.DESCRIPTION
    Modifies the registry so that myshows callback URI can be automatically sent to myshows-python3
#>

function Set-RegistryKey ($Path, $Name, $Value) {
    if (-NOT (Test-Path $Path)) {
        New-Item $Path -Force
    }
    if ($Name -eq $null) {
        Set-Item -Path $Path -Value $Value -Force #Set (Default) value
    } else {
        New-ItemProperty -Path $Path -Name $Name -Value $Value -PropertyType ExpandString -Force
    }
}

$python = (Get-Command python).Path
New-PSDrive -Name HKCR -PSProvider Registry -Root HKEY_CLASSES_ROOT 
Set-RegistryKey -Path "HKCR:\myshows" -Name "URL Protocol" -Value ""
Set-RegistryKey -Path "HKCR:\myshows\shell\open\command" -Value "`"$python`" `"-m`" `"myshows`" %1"