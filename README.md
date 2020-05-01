# get_proc_count.py
A simple utility for translating the CPU quota provided to Nomad tasks into a _rough_ equivalent number of processors. This can be useful when dynamically deciding how many threads to launch.

# Example Usage
The below is taken from a simple Docker entrypoint script for running MLFlow. 

```
#!/bin/bash 
set -x
export GOOGLE_APPLICATION_CREDENTIALS=/service_account.json
PROC_COUNT=$(/usr/local/bin/get_proc_count.py)
mlflow server --host 0.0.0.0 --workers $PROC_COUNT "$@"
```

Another example taken from a CI job running `make`:
```
CPU_COUNT=$(/usr/local/bin/get_proc_count.py)
SAFE_CPU_COUNT=$(($CPU_COUNT/2))
make -j $SAFE_CPU_COUNT
```
