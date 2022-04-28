#!/usr/bin/env python3
"""vSphere Python SDK script - show all VM parents"""

import sys
import ssl
import atexit
import config
from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, SmartConnect, Disconnect


def main():
    """main section"""

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
            print(msg)
            return -1

        atexit.register(Disconnect, service_instance)
        content = service_instance.RetrieveContent()

        # Search for all parents
        objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)

        vm_list = objview.view
        objview.Destroy()

        counter = 0
        parents_list = []
        print("Searching all parents, this can take some time, please wait ...")
        for vm in vm_list:

            try:
                parent = vm.parent.name
            except:
                parent = None

            if parent is not None and parent not in parents_list:
                parents_list.append(parent)

        for unique_parent in parents_list:
            counter += 1
            print("Parent #{}: {}".format(counter, unique_parent))

    except Exception as error:
        print(error, file=sys.stderr)
        print('Unable to connect to vsphere server.', file=sys.stderr)
        sys.exit(1)

    return 0


# Start program
if __name__ == "__main__":
    main()
