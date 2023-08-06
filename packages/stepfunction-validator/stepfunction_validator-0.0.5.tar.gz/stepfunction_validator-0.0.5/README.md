# Step Function Validator for e.g. (AWS)

An issue we have is that we are quite human and we often make mistakes in the YAML "code". 
These could be syntactical errors (for example, an incorrect indent), but also semantical (for example, forgetting to add a required parameter to a step). 
We only find out about these errors in the last step of the CI/CD, when the step function fails to deploy to AWS. This makes troubleshooting very.. slow...

So we came up with this little tool. 

## Authors

- [@b0tting](https://github.com/b0tting)
- [@NileshDebix](https://github.com/NileshDebix)


## Installation

1. create virtual environment in python and activate this one in Terminal or CMD

```python
  python3 -m venv env
  
  Windows: 
    
    env\Script\activate.bat

  Mac/Linux:

    source env/bin/activate
```

2. pip install the tool via pypi

```python
    ####################### [ NOTE !!! ] ############################################################
    #    you NEED to see in your command line the env before your prompt
    #    so you know that you are in your virtual environment:
    #
    #    example: (env) niels@Mac%
    ################################################################################################

    if above is clear then:

    pip install stepfunction-validator or pip3 install stepfunction-validator # to install the required libraries and the tool

```


## Usage/Examples

```python
     stepfunction_validator.exe [-s test.yaml] [-j <stepfunctions_schema.json>] [--no-lint]    
```
This will validate a YAML file against the schema you provided in the CLI. If the -c parameter is omitted, the script runs against every .yml file it can find in the current working directory. A default schema for AWS stepfunctions is included, but an overriding schema can be passed with the -j parameters. Skip linting with "--no-lint". If any linting, syntax or schema errors are found an exit code 1 will be returned with a list of errors found. Example output:
``` 
.\test\step_function_invalid.yml:1:missing document start "---" (document-start)
.\test\step_function_invalid.yml:1:no new line character at the end of file (new-line-at-end-of-file)
.\test\step_function_invalid.yml:'Pass' is not one of ['Choice']. Failed validating enum in deque([0, 'properties', 'Type', 'enum']): {'type': 'string', 'enum': ['Choice']}
```

