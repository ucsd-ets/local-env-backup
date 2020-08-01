from jupyter_client.kernelspec import KernelSpecManager
import subprocess
import os, json


def kernel_exists(kernel_name):
    manager = KernelSpecManager()
    return kernel_name in manager.find_kernel_specs().keys()


def get_kernel_location(kernel_name):
    if kernel_exists(kernel_name):
        manager = KernelSpecManager()
        return manager.get_kernel_spec(kernel_name).resource_dir
    else:
        from jupyter_client.kernelspec import NoSuchKernel
        raise NoSuchKernel(kernel_name)


def get_kernel_env(kernel_name):
    config_loc = os.path.join(get_kernel_location(kernel_name), 'kernel.json')
    config = json.load(open(config_loc))
    if 'env' in config:
        return config['env']
    else:
        return {}


def get_userbase(kernel_name):
    env = get_kernel_env(kernel_name)
    if 'PYTHONUSERBASE' in env:
        return env['PYTHONUSERBASE']
    else:
        return None


def set_userbase(kernel_name, userbase):
    config_loc = os.path.join(get_kernel_location(kernel_name), 'kernel.json')
    config = json.load(open(config_loc))
    if not 'env' in config:
        config['env'] = {'PYTHONUSERBASE': userbase}
    else:
        config['env']['PYTHONUSERBASE'] = userbase
    json.dump(config, open(config_loc, 'w'), indent=2)


def install_new_ipykernel(name, disp_name):
    cmd = subprocess.run([
        'ipython', 'kernel', 'install',
        '--name', name,
        '--display-name', disp_name,
        '--user'
    ], capture_output=True)

    if cmd.returncode == 0:
        print(cmd.stdout.decode(), end='')
    else:
        print(cmd.stderr.decode())
        raise AssertionError

    # return kernel location
    return cmd.stdout.decode().split(' ')[-1]


def install_launch_script(kernel_name):
    env = get_kernel_env(kernel_name)
    kernel_loc = get_kernel_location(kernel_name)
    script_fp = open(os.path.join(kernel_loc, 'activate.sh'), 'w')
    script_fp.write('set -a\n')
    script_fp.write(
        '\n'.join([f'{k}={v}' for k, v in env.items()])
    )
    script_fp.close()
