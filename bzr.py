#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2014, Wes Mason <wesley.mason@canonical.com>
#
# You should have received a copy of the GNU General Public License
# along with ansible-bzr. If not, see <http://www.gnu.org/licenses/>.
#

DOCUMENTATION = '''
---
module: bzr
short_description: Manages and interacts with bazaar repositories
description:
    - "Manage bzr/bazaar repositories. To use this module, the
      following keys are required: C(src) and C(path)."
'''

EXAMPLES = '''
'''

def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(default=None, required=True),
            path=dict(default=None, required=True),
            branch=dict(default='yes', type='bool', required=False),
            update=dict(default='yes', type='bool', required=False),
            extra_args=dict(default=None, required=False),
        ),
        supports_check_mode=True
    )

    src = module.params['src']
    path = module.params['path']
    branch = module.params['branch']
    update = module.params['update']
    extra_args = module.params['extra_args']

    changed = False
    cmd = ''
    out = ''
    err = ''

    module.exit_json(changed=changed, cmd=cmd, src=src, path=path,
                     stdout=out, stderr=err)



# import module snippets
from ansible.module_utils.basic import *

main()
