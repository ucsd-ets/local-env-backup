import argparse
import sys, os, subprocess

from env_backup.src.kernel import kernel_exists, kernel_location, install_new_ipykernel, \
    set_userbase, get_userbase
from env_backup.src.util import fmt_now, backup_local, valid_label, remove_local, \
    _kernel_name_description, prompt_proceed



def new_kernel(args):
    if not valid_label(args.name):
        print(_kernel_name_description, file=sys.stderr)
        sys.exit(1)

    kernel_name = f'python3_{args.name}'
    display_name = f'Python 3 ({args.name})'
    local_backup_dir = os.path.expanduser(f'~/.local_backup_{kernel_name}')

    if kernel_exists(kernel_name):
        print(f'Kernel {kernel_name} already exists.')
        prompt_proceed(f'-> Replace the content in {kernel_name}? (y/n) ')
    
    if os.path.exists(local_backup_dir):
        print(f'Backup in {local_backup_dir} already exists.')
        prompt_proceed(f'-> Replace the content in {local_backup_dir}? (y/n) ')


    print('\n'.join([
        'New kernel information:',
        f'  Kernel name: "{kernel_name}"',
        f'  Display name: "{display_name}"',
        f'  Install location: "~/.local/shared/jupyter/kernels/{kernel_name}"',
        f'  .local backup location: "{local_backup_dir}"'
    ]))

    prompt_proceed("-> Ready to proceed? (y/n) ")

    print()
    install_new_ipykernel(kernel_name, display_name)
    backup_local(dest=local_backup_dir)
    set_userbase(kernel_name, local_backup_dir)

    prompt_proceed("-> Remove python dependencies in ~/.local? (y/n) ")
    remove_local(None)
    print('Done')


def list_kernel(args):
    cmd = subprocess.run([
        'jupyter', 'kernelspec', 'list'
    ], capture_output=True)

    print(cmd.stdout.decode(), end='')


def activate_kernel(args):
    kernel_name = args.kernel_name
    userbase = get_userbase(kernel_name)
    if userbase:
        print(f'PYTHONUSERBASE={userbase}')
        print(f"echo 'Success, kernel {kernel_name} activated'")
    else:
        print(f"echo 'PYTHONUSERBASE not set in kernel \"{kernel_name}\"'")


def main():
    parser = argparse.ArgumentParser(prog='env-backup')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_a = subparsers.add_parser('new', help='a help')
    parser_a.add_argument('--name', default=fmt_now(), help='bar help')
    # parser_a.add_argument('--yes')
    parser_a.set_defaults(func=new_kernel)

    parser_b = subparsers.add_parser('list', help='b help')
    parser_b.set_defaults(func=list_kernel)

    parser_c = subparsers.add_parser('activate')
    parser_c.add_argument('kernel_name')
    parser_c.set_defaults(func=activate_kernel)

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()