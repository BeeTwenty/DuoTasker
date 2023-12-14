Get-ChildItem "C:\Users\sindr\Documents\DuoTasker" -Recurse | ForEach-Object {
    if (-Not $_.PSIsContainer) {
        $content = Get-Content $_.FullName
        $content | Set-Content -Encoding utf8 $_.FullName
        (Get-Content $_.FullName) -replace "`r`n", "`n" | Set-Content $_.FullName
    }
}
