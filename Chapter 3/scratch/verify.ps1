$html = Get-Content 'chapter3.html' -Encoding UTF8
"Total lines: $(($html).Count)"
"Proof boxes: $(($html | Select-String 'proof-box' | Measure-Object).Count)"
"Example layout divs: $(($html | Select-String 'example-problem-layout' | Measure-Object).Count)"
"Sol toggles: $(($html | Select-String 'sol-toggle' | Measure-Object).Count)"
