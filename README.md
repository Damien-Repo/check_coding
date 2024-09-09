# Check coding

## Introduction

*(in tribute to MLE)*

This tool can be used to check coding style of C source files.

The objective of this tool is to give the possibility for anyone to create any rules.
You can use default checkers (customized with configuration file) or use your own custom checkers.

## How to install

```
pip install -r Requirements.txt
```

## How to run

- To validate a file:
```
./app.py file.c
```

- To validate a file with a specific configuration:
```
./app.py -c custom/conf/example/conf_example.py test_file.c
```

- To display the configuration used during the validation:
```
./app.py -c custom/conf/example/conf_example.py -d -- test_file.c
./app.py -c custom/conf/example/conf_example.py -d str test_file.c
./app.py -c custom/conf/example/conf_example.py -d json test_file.c
```

- To display all options:
```
./app.py --help
```

## libclang

To use AST based checkers, you need libclang and specify the path to the config file.

```
{
  "ConfigExample": {
    "Loader": {
      "Clang": {
        "LIB_PATH": "/usr/lib/llvm-14/lib/libclang-14.so"
      }
    }
  }
}
```

Tested with libclang version 14.

- Note: in the future libclang will be automatically detected or embedded

## Arborescence

```
check_coding/
├── app.py*                    # Program to launch
├── custom/                    # Custom folder with your own "things"
│   ├── checkers/              # Your custom checkers
│   ├── conf/                  # Your custom configuration
│   ├── filetypes/             # Your custom filetypes folder
│   ├── loaders/               # Your custom loaders
│   └── utests/                # Your unit tests for your custom checkers
└── lib/                       # Source code of the program
    ├── check_coding.py        # Defines CheckCoding class
    ├── checkers/              # Internal checkers folder
    │   ├── default/           # Default checkers folder
    │   └── ichecker.py        # Interface class for each checker
    ├── config/                # Internal configuration folder
    │   ├── default/           # Default configuration folder
    │   ├── iconfig.py         # Interface class for each configuration
    │   └── loaders/           # Internal configuration loaders folder
    ├── filetypes/             # Internal filetypes folder
    │   ├── default/           # Default filetypes folder
    │   └── ifiletype.py       # Interface class for each filetype
    ├── icheck_exception.py    # Interface class for each checker exception
    ├── loaders/               # Internal loaders folder
    │   ├── default/           # Default loaders folder
    │   └── iloader.py         # Interface class for each loader
    ├── log.py                 # Internal log class
    ├── outcomes/              # Internal outcomes folder
    │   ├── default/           # Default outcomes folder
    │   └── ioutcome.py        # Interface class for each outcome
    ├── source_file.py         # Internal source file class
    └── utests/                # Internal unit tests folder
        └── checkers/          # Internal unit tests folder for each default checkers
```

## TODO

- add FileTypes:
  - allow adding custom types (with custom filepath associated)

- add default checkers
  - ANSSI norm
  - other?

- add custom checkers
  - FCPP norm (for tool testing)

- allow configuring compilation options globally and per file

- create a unique ID system for each error (to allow the caller to acknowledge a list of errors for example)
  - must be able to create dynamic IDs even for custom ones
  - should be able to keep ID uniqueness even from one config to another
  - see if we should have easily readable IDs (like CRC32) so they are humanly identifiable or not (like SHA512)
  - in the spirit of Coverity tool CIDs

- test on many large files with all checkers to see if performances are ok

