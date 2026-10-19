#script.ps1
param([String]$folderpath, [String]$livetime, [String]$filename, [String]$function)
Write-Output $folderpath
Write-Output $livetime
Write-Output $filename
Write-Output $function
wsl /mnt/c/Users/XCF/Desktop/CrisPy/onWsl/launch.sh $folderpath $livetime $filename $function
