from jupyter_client.kernelspec import KernelSpecManager
import subprocess
import os, json


def kernel_exists(kernel_name):
    manager = KernelSpecManager()
    return kernel_name in manager.find_kernel_specs().keys()


def kernel_location(kernel_name):
    if kernel_exists(kernel_name):
        manager = KernelSpecManager()
        return manager.get_kernel_spec(kernel_name).resource_dir
    else:
        from jupyter_client.kernelspec import NoSuchKernel
        raise NoSuchKernel(kernel_name)


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


def set_userbase(kernel_name, userbase):
    config_loc = os.path.join(kernel_location(kernel_name), 'kernel.json')
    config = json.load(open(config_loc))
    if not 'env' in config:
        config['env'] = {'PYTHONUSERBASE': userbase}
    else:
        config['env']['PYTHONUSERBASE'] = userbase
    json.dump(config, open(config_loc, 'w'), indent=2)
    print(json.dumps(config, indent=2))



def get_userbase(kernel_name):
    config_loc = os.path.join(kernel_location(kernel_name), 'kernel.json')
    config = json.load(open(config_loc))
    if 'env' in config:
        if 'PYTHONUSERBASE' in config['env']:
            return config['env']['PYTHONUSERBASE']
    else:
        return