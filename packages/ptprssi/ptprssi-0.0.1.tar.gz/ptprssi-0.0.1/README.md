![penterepTools](https://www.penterep.com/external/penterepToolsLogo.png)


# PTPRSSI
> Path-relative Style Sheet Import Testing Tool

ptprssi is a tool for testing path-relative style sheet vulnerabilities.

## Installation

```
pip install ptprssi
```

## Usage examples
```
prssi -u https://www.example.com/
ptprssi -u https://www.example.com/ -r
```

## Options
```
-u   --url         <url>           Connect to URL
-r   --redirects                   Follow redirects
-p   --proxy       <proxy>         Set proxy (e.g. http://127.0.0.1:8080)
-H   --headers     <header:value>  Set custom header(s)
-ua  --user-agent  <ua>            Set User-Agent header
-c   --cookie      <cookie>        Set cookie
-j   --json                        Output in JSON format
-v   --version                     Show script version and exit
-h   --help                        Show this help message and exit
```

## Dependencies
```
ptlibs
requests
lxml
bs4
```

## Dependencies
   - bs4
   - lxml
   - requests
   - ptlibs

## Version History
    0.0.1
        Alpha release

## Licence

Copyright (c) 2020 HACKER Consulting s.r.o.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

## Warning

You are only allowed to run the tool against the websites which
you have been given permission to pentest. We do not accept any
responsibility for any damage/harm that this application causes to your
computer, or your network. Penterep is not responsible for any illegal
or malicious use of this code. Be Ethical!