#!/usr/bin/env python3
"""
vSphere Python SDK script - shutting down selected VMs
"""

import os
import ssl
import atexit
from datetime import datetime
import config
import whitelist
from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, SmartConnect, Disconnect

# Variables and constants
LOG_FILE = datetime.now().strftime('shut_down_vm_%d-%m-%Y_%H:%M:%S.log')
LOG_FILE_PATH = os.path.join(config.logs, LOG_FILE)

# activate log
log_file_object = open(LOG_FILE_PATH, 'a')


def show_and_append_to_log(log_message: str):
    """add date/time and some message to log file"""
    date_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(log_message)
    log_file_object.write(f'\n{date_time} - {log_message}')


def main():
    """main section"""

    show_and_append_to_log("VM shutdown tool started.")
    service_instance = None
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

    try:
        if config.no_ssl_verify:
            service_instance = SmartConnectNoSSL(
                host=config.host,
                user=config.user,
                pwd=config.pwd,
                port=int(config.port),
                certFile=None,
                keyFile=None,
            )
        else:
            service_instance = SmartConnect(
                host=config.host,
                user=config.user,
                pwd=config.pwd,
                port=int(config.port),
                sslContext=context,
            )

        if not service_instance:
            msg = ("Could not connect to the specified host using specified "
                   f"host [{config.host}], username [{config.user}]")
            show_and_append_to_log(msg)
            return -1

        atexit.register(Disconnect, service_instance)
        content = service_instance.RetrieveContent()

        # Search for all VMs
        objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)

        vm_list = objview.view
        vm_total = len(vm_list)
        objview.Destroy()

        protected_vms = []
        protected_vms = whitelist.whitelist_vms

        count_white_listed = 0
        processed = 0
        show_and_append_to_log("Processing VMs, this can take some time, please wait ...")
        for vm in vm_list:

            try:
                parent = vm.parent.name
            except:
                parent = None

            if parent is not None and parent in config.required_parents:
                processed += 1
                if str(vm.name) not in protected_vms:
                    show_and_append_to_log("Suspending VM #{}: {}".format(processed, vm.name))
                    vm.ShutdownGuest()
                else:
                    show_and_append_to_log(f"VM [{vm.name}] found on the whitelist."
                                           " Leaving without any change.")
                    count_white_listed += 1

        show_and_append_to_log('-' * 40 + ' STATISTICS ' + '-' * 40)
        show_and_append_to_log(f"On VMware vSphere found [{vm_total}] virtual machines.")
        show_and_append_to_log(f"Processed [{processed}] virtual machines for requested"
                               f" parents [{config.required_parents}].")
        show_and_append_to_log(f"Skipped/whitelisted [{count_white_listed}] virtual machines.")

    except Exception as error:
        show_and_append_to_log('Unable to connect to vsphere server.')
        show_and_append_to_log(error)

    show_and_append_to_log("VM shutdown tool finished.")

    # Close log file
    log_file_object.close()

    return 0


# Start program
if __name__ == "__main__":
    main()
