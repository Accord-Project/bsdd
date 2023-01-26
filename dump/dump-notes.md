# Dump Size
Ontotext\project\ACCORD\bSDD\data\graphql-2023-01-24.zip:
- json, no spaces, 32Mb zipped.
- 30465 files, 253Mb unzipped:
  - domains: 203Mb, 30k files
  - REST: 50Mb, 6 files

## RDFize
```
sparql-anything.bat -q ../scripts/rdfize-zip.sparql -v zip=graphql-2023-01-24.zip > raw-rdf.ttl
```

## Filename Problem
Fails on `domains\gsa_gsaspace-23\CON.json`. Microsoft are fucking idiots: all these are invalid filenames:
```
CON, PRN, AUX, CLOCK$, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9
```

Let's look for such bad names:
```
sparql-anything.bat -q ../scripts/list-zip.sparql -v zip=graphql-2023-01-24.zip | grep -Pi "\b(CON|PRN|AUX|CLOCK|NUL|COM\d|LPT\d)\b"
domains/gsa_gsaspace-23/CON.json
```

Misho renamed it to `COM.json`

## Empty Folder Problem
`domains/csi_omniclass-1` is an empty folder:
```
ERROR com.github.sparqlanything.cli.SPARQLAnything - Iteration 1 failed with error: java.io.IOException: java.io.FileNotFoundException: tmp\9c7edbb4c5428e0901712bba87769bf1\domains\csi_omniclass-1 (Access is denied)
```
Deleted it.

Then it failed on `domains/nlsfb_nlsfb2005-2.2` and I can't see anything wrong with this file.
So I wrote a batch file to do it domain by domain, and moved `domains/nlsfb_nlsfb2005-2.2` last

## Mixup Absolute/Relative URL

https://github.com/SPARQL-Anything/sparql.anything/issues/335

It fails with the following error:

```
[main] ERROR com.github.sparqlanything.engine.FacadeXOpExecutor - An error occurred: 
java.io.FileNotFoundException: 
tmp\cd81ed69fe4de812bb3928afd960e85d\http:\sparql.xyz\facade-x\ns\root 
(The filename, directory name, or volume label syntax is incorrect)

[main] ERROR com.github.sparqlanything.cli.SPARQLAnything - Iteration 1 failed with error: 
java.io.IOException: java.io.FileNotFoundException:
 tmp\cd81ed69fe4de812bb3928afd960e85d\http:\sparql.xyz\facade-x\ns\root 
(The filename, directory name, or volume label syntax is incorrect)
```
