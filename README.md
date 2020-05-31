# pdfaudit
PDF file security and privacy auditing tool written in Python

The tool parses a pdf file looking for the following keys:
(GoTo), GoToR and GoToE,
Launch,
URI,
SumbitForm,
JavaScript,
OpenAction,
AA

PDFaudit outputs the content of the corresponding values and object location to aid assessment of security and privacy risks. 

The tool is currently in development, with currently about 80% of the required code implemented. The pdf standard has multiple options to store document information, which makes it a challenge to cover all possible scenario's. Moreover, the document specification is at some instances less consicely defined, making room for multiple interpretations. Combined with the current development phase of pdfaudit, a high succes rate can not yet be guaranteed of the tool parsing each pdf correctly in the first place, and detecting and reporting the security and privacy threats. The end goal however is to be compatible with at least the ISO 32000-1:2008, which covers PDF versions up to and including PDF1.7

### Prerequisites

PDFaudit is written in Python, and uses Python3 code

```
TBD
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```


### TODO list
1) DCTDecode filter
2) Refactoring iterations in general
3) Speed optimizations (like don't uncompress if not needed)
4) Determine if a split between high and low-risk threats is useful
5) Check/improve object scanning and numbering
6) Summarize exceptions that occurred using filters
7) Linearized pdf's

## Version History
#### v0.6 31 May 2020
##### New:
- Scans pdf for objects independent of cross reference tables. Hardening / handling of malformed pdf's: ability to handle incorrect location of xref, reference to incorrect location of objects, of non-existent objects. 
##### Bugfixes
- Filter function is now byte-wise (resulting in incorrect object numbers, locations, etc)


#### v0.5 30 May 2020
##### New:
- Output number of scanned objects
- Checks pdf header
- Handling of escaped backlashes in literal strings, translation of hexadecimal strings, and hex characters in names (obfuscation)
- Printing non-printable characters (verbosity >1)
- Ability to find cross reference tables despite incorrect position references to them
- Option to print pdf document structure to screen with object locations
##### Bugfixes
- Crossreference lists not used as global variables in functions
- Comment handling for some EOF situations


#### v0.4 22 May 2020
##### New:
- /OpenAction and /AA
##### Bugfixes
- Fixed incorrect escape handling in strings 


#### v0.3: 21 May 2020
##### New: 
- Ability to scan object streams
- Some speed optimizations
##### Bugfixes:
- Only read DecodeParms if they exist
- EOF was not handled correctly in readword function


#### v0.2: 20 May 2020
##### New:
- Ability to read cross reference streams


#### v0.1
First rudimentary version


## License

pdfaudit Copyright (C) 2020 Joseph Heller

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

## Acknowledgments

* Didier Stevens for sharing his knowledge on malicious pdf files
* Yusuke Shinyama, for some of the decoding filters from pdfminer





