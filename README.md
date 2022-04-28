# Shutdown VMs tool purpose
Purpose of this tool is to keep HW requirement on lowest level.
Therefore this tool shutdown all VMs which are not in the whitelist file.
This scrip is trying to keep number of requirements on minimal level.


## Tool expected usage
Tool should be added to linux cronjob or any other scheduler and executed periodically (on daily bases). Tool have a possibility to exclude VMs (protect them from shutdown).

## Prerequisites
* Python3
* Additional modules

To install necessary Python modules use command:

```bash
pip3 install -r requirements.txt
```

## Setup
There are only 2 things you need to do :
* modify config.py file (insert credentials and other VMware server parameters)
* in file whitelist.py define VMs which should be on the whitelist (those will be ignored within shutdown procedure)
* **HINT**: To be save first try to run show_all_vms.py and show_all_parents.py before you run shutdown tool.

**Values in config.py:**
* no_ssl_verify - ssl verification, by default is ssl enabled
* host - VMware vSphere server (FQDN or IP)
* user - VMware vSphere user
* pwd - VMware vSphere password
* port - VMware vSphere port (by default it's 443)
* required_parents - it is a list of required parents which will be suspended (parents which are not mentioned on that list will be ignored)
* logs - identify place where logs will be created

## Execution
Simply run following command:
```bash
cd TO_SHUTDOWN_VM_FOLDER ; ./shutdown_vm.py
```

## Other tools
There are also two other scripts:
* show_all_vms.py - list all available VMs together with parent name
* show_all_resource_parents.py - list alls available parents

## Limitations
* Script shutdown_vm.py produce log files. Default logging folder is 'logs'. You can change log folder in config.py. For each execution of shutdown_vm.py is generated new log file.
* using own logging mechanism to keep number of dependencies on minimal level

## Sponsoring

Many thanks **Elevēo** for support this project.

[![Elevēo - powered by ZOOM International](img/eleveo-logo.png)](https://eleveo.com)