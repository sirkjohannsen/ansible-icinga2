#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016, Sirk Johannsen <svensirk@gmail.com>
#
# This file extends Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>


import subprocess
import shlex

DOCUMENTATION = '''
This module gives access to the icinga2 feature functionality and allows enabling and disabling of features
'''
EXAMPLES = '''
 - name: Enable/Disable Icinga2 Web ido-mysql and command features
   icinga2_feature: feature={{ item }} action={{ icinga_feature }}
   with_items:
     - 'ido-mysql'
     - 'command'

 - name: Enable/Disable Icinga2 API
   icinga2_feature: feature=api action={{ icinga2_api }}

'''

RETURN = '''
returns 
 success: True/False
 returncode: Returncode of the command
 output: stdout and stderr
 command: The execured command
'''

def main():
    module = AnsibleModule(
        argument_spec = dict(
            feature         = dict(required=True, aliases=['name']),
            action      = dict(default="enable", options=['enable', 'disable']),
        ),
        supports_check_mode=True,
    )

    params = module.params
    # Set defaults
    fchanged = False
    fsuccess = True

    rcommand = "/usr/sbin/icinga2 feature list | grep " + params['feature'] + " | grep -i " + params['action']
    checkcmd = subprocess.Popen(rcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    checkresult = checkcmd.communicate()
    freturn = checkcmd.returncode
    fstdout = checkresult[0] + " : " + checkresult[1]
    if checkcmd.returncode != 0 :
        rcommand = "/usr/sbin/icinga2 feature " + params['action'] + " " + params['feature']
        fcmd = subprocess.Popen(rcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        fresult = fcmd.communicate()
        freturn = fcmd.returncode
        fstdout = fresult[0] + " : " + fresult[1]
        if fcmd.returncode != 0 :
            fsuccess = False
        else :
            fchanged = True

    if fsuccess :
        module.exit_json(changed=fchanged, success=fsuccess, returncode=freturn, output=fstdout, command=rcommand)
    else :
        module.fail_json(msg=fstdout)

# import module snippets
from ansible.module_utils.basic import *
main()
