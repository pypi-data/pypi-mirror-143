# ukbsearch

Search tools to retreive term(s) from UKB HTML files to be downloaded in the local drive.

## Installation

```
pip install https://github.com/danielmsk/ukbsearch/dist/ukbsearch-0.0.1-py3-none-any.whl
pip install ukbsearch
```

## Options
```
optional arguments:
  -h, --help            show this help message and exit
  
  -v, --version         show program's version number and exit
  
  -s, --searchterm      search. terms (ex: age smoking)
                        -s age
                        -s age smoking
                        -s 'smok*'
                        -s '*age' 'smok*'
                        
  -l, --logic           logical operator for multiple terms [or(default), and]
                        -s '*age' 'smok*' -l and
                        -s age 'smok*' -l or
  
  -o, --out             title of output file
                        -o searchresult_20220322
  
  -t, --outtype         output type [console(default), csv, udi]
                        -t csv
                        -t console csv
                        -t udi
                        -t console udi
  
  -p, --path            directory path for data files (.html, .Rdata) (default: ./)
                        -p /other/path/for/ukb/html/.
  
  -u, --udilist         FileID and UDI list for saving data from RData files
                        -u ukb39003 3536-0.0 3536-1.0 3536-2.0
  
  -d, --savedata        save data from .Rdata [csv, rdata]
                        -d csv 
                        -d rdata
                        -d csv rdata
```




## Usage

### Search result
![](https://raw.githubusercontent.com/danielmsk/ukbsearch/main/docs/screenshot1.png?token=GHSAT0AAAAAABSGIZOM3KNUUTFMR4HLUQHMYRZRPCQ)


### Search for single term
```
ukbsearch -s age
ukbsearch --searchterm age
ukbsearch -s 'ag*'
ukbsearch -s '*ge' 
```

### Search for multiple terms
* The logical operators (`and` or `or`) are supported.

```
ukbsearch -s age smoking
ukbsearch -s age smoking -l or
ukbsearch -s age smoking -l and
ukbsearch -s 'ag*' 'smok*' -l and 
```

### Print only html and UDI 
```
ukbsearch -s 'ag*' 'smok*' -l and -t udi
```

### Save the search result as csv file
```
ukbsearch -s 'ag*' 'rep*' -l and -o test1 -t csv
(= ukbsearch --searchterm 'ag*' 'rep*' --logic and --out test1 --outtype csv)
ukbsearch -s 'ag*' 'rep*' -l and -o test1 -t console csv
ukbsearch -s 'ag*' 'rep*' -l and -o test1 -t console udi csv
```

### Set a particular directory
* The default path is './'.

```
ukbsearch -s age -p /other/path/for/ukb/html/.
```


### Save data (.csv and .rdata) from .RData
```
ukbsearch -u ukb39003 3536-0.0 3536-1.0 3536-2.0 -d csv -o test3
(=ukbsearch --udilist ukb39003 3536-0.0 3536-1.0 3536-2.0 --savedata csv --out test3)
ukbsearch -u ukb39003 3536-0.0 3536-1.0 ukb26086 20161-0.0 21003-1.0 -d csv rdata -o test3

ukbsearch -s 'ag*' 'rep*' -l and -d csv -o test3
ukbsearch -s 'ag*' 'rep*' -l and -d rdata -o test3
```



