#!/usr/bin/env python
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

def _fail(module, cmd, out, err):
    msg = ''
    if out:
        msg += "stdout: %s" % (out, )
    if err:
        msg += "\n:stderr: %s" % (err, )
    module.fail_json(cmd=cmd, msg=msg)


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
            extra_args=dict(default=None, required=False),
        ),
        mutually_exclusive=[['tag', 'revision']],
        supports_check_mode=True,
    )

    src = module.params['src']
    path = module.params['path']
    state = module.params['state']
    revision = module.params['revision']
    tag = module.params['tag']
    overwrite = module.params['overwrite']
    extra_args = module.params['extra_args']

    changed = False
    cmd = ''
    out = ''
    err = ''

    if tag:
        if 'tag:' not in tag:
            tag = 'tag:{}'.format(tag)

        revision = tag

    if revision:
        extra_args += ' --revision={}'.format(revision or tag)

    path_exists = os.path.exists(path)

    if not path_exists:
        cmd = 'bzr branch {} {} {}'.format(extra_args, src, path)
        rc, out, err = module.run_command(cmd)
        changed = True

        if rc != 0:
            _fail(module, rc, out, err)

    elif revision or state == 'latest':
        update = True

        if revision:
            cmd = 'bzr revno --tree {}'.format(path)
            rc, out, err = module.run_command(cmd)

            if rc != 0:
                _fail(module, rc, out, err)

            if out.strip() != revision:
                update = True

        if update:
            if overwrite:
                extra_args += ' --overwrite'

            cmd = 'bzr pull {} {} -d {}'.format(extra_args, src, path)
            rc, out, err = module.run_command(cmd)

            if rc != 0:
                _fail(module, rc, out, err)

            if 'Now on revision' in out:
                changed = True


    module.exit_json(changed=changed, cmd=cmd, src=src,
                     path=path, revision=revision, stdout=out, stderr=err)


# import module snippets
from ansible.module_utils.basic import *

main()
