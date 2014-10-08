#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2014, Wes Mason <wesley.mason@canonical.com>
#
# You should have received a copy of the GNU General Public License
# along with ansible-bzr. If not, see <http://www.gnu.org/licenses/>.
#

import os


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
    states = 'present', 'latest',

    module = AnsibleModule(
        argument_spec=dict(
            src=dict(default=None, required=True),
            path=dict(default=None, required=True),
            state=dict(default='latest', choices=states, required=False),
            revision=dict(default=None, required=False),
            tag=dict(default=None, required=False),
            overwrite=dict(default=False, required=False),
            checkout=dict(default=False, required=False),
            extra_args=dict(default=None, required=False),
        ),
        supports_check_mode=True
    )

    src = module.params['src']
    path = module.params['path']
    state = module.params['state']
    revision = module.params['revision']
    tag = module.params['tag']
    overwrite = module.params['overwrite']
    checkout = module.params['checkout']
    extra_args = module.params['extra_args']

    changed = False
    cmd = ''
    out = ''
    err = ''

    path_exists = os.path.exists(path)

    module.exit_json(changed=changed, cmd=cmd, src=src, path=path,
                     revision=revision, stdout=out, stderr=err)


# import module snippets
from ansible.module_utils.basic import *

main()
