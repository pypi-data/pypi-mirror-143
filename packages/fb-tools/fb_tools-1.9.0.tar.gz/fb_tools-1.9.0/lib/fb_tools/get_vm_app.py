#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Frank Brehm
@contact: frank.brehm@pixelpark.com
@copyright: © 2021 by Frank Brehm, Berlin
@summary: The module for the application object.
"""
from __future__ import absolute_import, print_function

# Standard modules
import logging
import getpass

from operator import attrgetter

# Third party modules
import pytz

# Own modules
from . import __version__ as GLOBAL_VERSION
from . import VMWARE_CFGFILE_BASENAME

from .xlate import XLATOR

from .common import pp

from .app import BaseApplication

from .config import CfgFileOptionAction

from .errors import FbAppError

from .vmware_config import VmwareConfiguration

from .vsphere.server import VsphereServer

from .vsphere.controller import VsphereDiskController

from .vsphere.ether import VsphereEthernetcard

__version__ = '1.4.2'
LOG = logging.getLogger(__name__)
TZ = pytz.timezone('Europe/Berlin')

_ = XLATOR.gettext
ngettext = XLATOR.ngettext


# =============================================================================
class GetVmAppError(FbAppError):
    """ Base exception class for all exceptions in this application."""
    pass


# =============================================================================
class GetVmApplication(BaseApplication):
    """
    Class for the application objects.
    """

    # -------------------------------------------------------------------------
    def __init__(
        self, appname=None, verbose=0, version=GLOBAL_VERSION, base_dir=None,
            initialized=False, usage=None, description=None,
            argparse_epilog=None, argparse_prefix_chars='-', env_prefix=None):

        desc = _(
            "Tries to get information about the given virtual machines in "
            "VMWare VSphere and print it out.")

        self._cfg_file = None
        self._cfg_dir = None
        self.config = None

        self.vsphere = {}

        self.vms = []

        super(GetVmApplication, self).__init__(
            appname=appname, verbose=verbose, version=version, base_dir=base_dir,
            description=desc, initialized=False,
        )

        self.initialized = True

    # -------------------------------------------------------------------------
    @property
    def cfg_dir(self):
        """Directory of the configuration file."""
        return self._cfg_dir

    # -------------------------------------------------------------------------
    @property
    def cfg_file(self):
        """Configuration file."""
        return self._cfg_file

    # -------------------------------------------------------------------------
    def as_dict(self, short=True):
        """
        Transforms the elements of the object into a dict

        @param short: don't include local properties in resulting dict.
        @type short: bool

        @return: structure as dict
        @rtype:  dict
        """

        res = super(GetVmApplication, self).as_dict(short=short)
        res['cfg_dir'] = self.cfg_dir
        res['cfg_file'] = self.cfg_file

        res['vsphere'] = {}
        for vsphere_name in self.vsphere:
            res['vsphere'][vsphere_name] = {}
            vsphere = self.vsphere[vsphere_name]
            if vsphere:
                res['vsphere'][vsphere_name] = vsphere.as_dict(short=short)

        return res

    # -------------------------------------------------------------------------
    def post_init(self):
        """
        Method to execute before calling run(). Here could be done some
        finishing actions after reading in commandline parameters,
        configuration a.s.o.

        This method could be overwritten by descendant classes, these
        methhods should allways include a call to post_init() of the
        parent class.

        """

        self.initialized = False

        self.init_logging()

        self._cfg_dir = self.base_dir.joinpath('etc')
        self._cfg_file = self.cfg_dir.joinpath(VMWARE_CFGFILE_BASENAME)

        self.perform_arg_parser()

        if not self.cfg_file.exists():
            default_conf_file = self.cfg_dir.joinpath(VMWARE_CFGFILE_BASENAME + '.default')
            msg = (_(
                "Configuration file {f!r} does not exists. Please copy {d!r} to {f!r} and "
                "fill out all necessary entries, e.g. the passwords.").format(
                    f=str(self.cfg_file), d=str(default_conf_file)))
            LOG.error(msg)
            self.exit(1)

        self.config = VmwareConfiguration(
            appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
            config_file=self.cfg_file)

        self.config.read()
        if self.config.verbose > self.verbose:
            self.verbose = self.config.verbose
        self.config.initialized = True

        if self.verbose > 3:
            LOG.debug("Read configuration:\n{}".format(pp(self.config.as_dict())))

        if not self.config.vsphere.keys():
            msg = (_(
                'Did not found any valid VSphere definition in {!r}.').format(self.cfg_file))
            LOG.error(msg)
            self.exit(1)

        for vsphere_name in self.config.vsphere.keys():
            vsphere_data = self.config.vsphere[vsphere_name]
            pw = None
            if 'password' in vsphere_data:
                pw = vsphere_data['password']
                if pw is None or pw == '':
                    prompt = (
                        _('Enter password for {n} VSPhere user {u!r} on host {h!r}:').format(
                            n=vsphere_name, u=vsphere_data['user'], h=vsphere_data['host'])) + ' '
                    vsphere_data['password'] = getpass.getpass(prompt=prompt)

        self.init_vsphere_handlers()

        self.initialized = True

    # -------------------------------------------------------------------------
    def init_arg_parser(self):
        """
        Public available method to initiate the argument parser.
        """

        super(GetVmApplication, self).init_arg_parser()

        self._cfg_dir = self.base_dir.joinpath('etc')
        self._cfg_file = self.cfg_dir.joinpath(VMWARE_CFGFILE_BASENAME)
        default_cfg_file = self.cfg_file

        self.arg_parser.add_argument(
            '-c', '--config', '--config-file', dest='cfg_file', metavar=_('FILE'),
            action=CfgFileOptionAction,
            help=_("Configuration file (default: {!r})").format(str(default_cfg_file))
        )

        self.arg_parser.add_argument(
            'vms', metavar='VM', type=str, nargs='+',
            help=_('Names of the VM to get information.'),
        )

    # -------------------------------------------------------------------------
    def perform_arg_parser(self):

        if self.verbose > 2:
            LOG.debug(_("Got command line arguments:") + '\n' + pp(self.args))

        if self.args.cfg_file:
            self._cfg_file = self.args.cfg_file

        for vm in self.args.vms:
            self.vms.append(vm)

    # -------------------------------------------------------------------------
    def init_vsphere_handlers(self):

        for vsphere_name in self.config.vsphere.keys():
            self.init_vsphere_handler(vsphere_name)

    # -------------------------------------------------------------------------
    def init_vsphere_handler(self, vsphere_name):

        vsphere_data = self.config.vsphere[vsphere_name]

        pwd = None
        if 'password' in vsphere_data:
            pwd = vsphere_data['password']

        vsphere = VsphereServer(
            appname=self.appname, verbose=self.verbose, base_dir=self.base_dir,
            host=vsphere_data['host'], port=vsphere_data['port'], dc=vsphere_data['dc'],
            user=vsphere_data['user'], password=pwd,
            auto_close=True, simulate=self.simulate, force=self.force,
            terminal_has_colors=self.terminal_has_colors, initialized=False)

        if vsphere:
            self.vsphere[vsphere_name] = vsphere
            vsphere.initialized = True
        else:
            msg = _("Could not initialize {} object from:").format('VsphereServer')
            msg += '\n' + pp(vsphere_data)
            LOG.error(msg)

    # -------------------------------------------------------------------------
    def _run(self):

        LOG.debug(_("Starting {a!r}, version {v!r} ...").format(
            a=self.appname, v=self.version))

        ret = 99
        try:
            ret = self.show_vms()
        finally:
            # Aufräumen ...
            for vsphere_name in self.config.vsphere.keys():
                LOG.debug(_("Closing VSPhere object {!r} ...").format(vsphere_name))
                self.vsphere[vsphere_name].disconnect()
                del self.vsphere[vsphere_name]

        self.exit(ret)

    # -------------------------------------------------------------------------
    def show_vms(self):

        ret = 0

        for vsphere_name in self.vsphere:
            vsphere = self.vsphere[vsphere_name]
            vsphere.get_datacenter()

        for vm_name in sorted(self.vms, key=str.lower):
            if not self.show_vm(vm_name):
                ret = 1

        return ret

    # -------------------------------------------------------------------------
    def show_vm(self, vm_name):

        print('\n{}: '.format(vm_name), end='')
        if self.verbose:
            print()
        vm = None
        for vsphere_name in self.vsphere:
            vsphere = self.vsphere[vsphere_name]
            vm = vsphere.get_vm(vm_name, vsphere_name=vsphere_name, no_error=True, as_obj=True)
            if vm:
                break

        if not vm:
            print(self.colored(_("NOT FOUND"), 'RED'))
            return False

        # print("{ok}\n{vm}".format(ok=self.colored("OK", 'GREEN'), vm=pp(vm.as_dict(bare=True))))
        print("{ok}".format(ok=self.colored("OK", 'GREEN')))
        print()
        print("    State:    {s:<13} Config version: {v}".format(
            s=vm.power_state, v=vm.config_version))
        msg = "    VSPhere:  {vs:<10}    Cluster: {cl:<20}    Path: {p}".format(
            vs=vm.vsphere, cl=vm.cluster_name, p=vm.path)
        print(msg)
        msg = (
            "    No. CPUs: {cp:4d}          RAM: {m:5.1f} GiB"
            "                   Cfg-Path: {p}").format(
                cp=vm.num_cpu, m=vm.memory_gb, p=vm.config_path)
        print(msg)
        print("    OS:       {id:<43}    {os}".format(id=vm.guest_id, os=vm.guest_fullname))
        first = True
        for ctrlr in sorted(
                filter(lambda x: x.scsi_ctrl_nr is not None, vm.controllers),
                key=attrgetter('bus_nr')):
            if ctrlr.scsi_ctrl_nr is None:
                continue
            label = ''
            if first:
                label = 'Controller:'
            first = False
            ctype = _('Unknown')
            if ctrlr.ctrl_type in VsphereDiskController.type_names.keys():
                ctype = VsphereDiskController.type_names[ctrlr.ctrl_type]
            no_disk = ngettext(" 1 disk ", "{>2} disks", len(ctrlr.devices)).format(
                len(ctrlr.devices))
            msg = "    {la:<15}  {nr:>2} - {di} - {ty}".format(
                la=label, nr=ctrlr.bus_nr, di=no_disk, ty=ctype)
            print(msg)

        if vm.disks:
            first = True
            for disk in vm.disks:
                label = ' ' * 15
                if first:
                    label = (ngettext('Disk', 'Disks', len(vm.disks)) + ':').ljust(15)
                first = False
                ctrlr_nr = -1
                for ctrlr in vm.controllers:
                    if disk.key in ctrlr.devices:
                        ctrlr_nr = ctrlr.bus_nr
                        break
                msg = "    {la}  {n:<15} - {s:5.1f} GiB - Controller {c:>2} - File {f}".format(
                    la=label, n=disk.label, s=disk.size_gb, c=ctrlr_nr, f=disk.file_name)
                print(msg)
        else:
            print("    Disks:       {}".format(_('None')))

        if vm.interfaces:
            first = True
            for dev in vm.interfaces:
                label = ' ' * 15
                if first:
                    label = 'Ethernet:'.ljust(15)
                first = False
                etype = _('Unknown')
                if dev.ether_type in VsphereEthernetcard.ether_types.keys():
                    etype = VsphereEthernetcard.ether_types[dev.ether_type]
                msg = "    {la}  {n:<15} - Network {nw:<20} - Connection: {c:<4} - {t}".format(
                    la=label, n=dev.label, nw=dev.backing_device, c=dev.connect_status, t=etype)
                print(msg)
        else:
            print("    Ethernet:    {}".format(_('None')))

        return True


# =============================================================================
if __name__ == "__main__":

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 list
