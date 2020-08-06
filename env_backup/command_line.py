import argparse
import sys, os, subprocess

from env_backup.src.kernel import kernel_exists, get_kernel_location, install_new_ipykernel, \
    set_userbase, get_userbase, install_launch_script
from env_backup.src.util import fmt_now, backup_local, valid_label, remove_local, \
    _kernel_name_description, prompt_proceed, prompt_proceed_exit, remove_dir



def new_kernel(args):
    if not valid_label(args.name):
        print(_kernel_name_description, file=sys.stderr)
        sys.exit(1)

    kernel_name = f'python3_{args.name}'
    display_name = f'Python 3 ({args.name})'
    local_backup_dir = os.path.expanduser(f'~/.local_backups/{kernel_name}')

    if kernel_exists(kernel_name):
        print(f'Kernel {kernel_name} already exists.')
        if not args.yes: prompt_proceed_exit(f'-> Replace the content in {kernel_name}? (y/n) ')
    
    if os.path.exists(local_backup_dir):
        print(f'Backup in {local_backup_dir} already exists.')
        if not args.yes: prompt_proceed_exit(f'-> Replace the content in {local_backup_dir}? (y/n) ')


    print('\n'.join([
        'New kernel information:',
        f'  Kernel name: "{kernel_name}"',
        f'  Display name: "{display_name}"',
        f'  Install location: "~/.local/shared/jupyter/kernels/{kernel_name}"',
        f'  .local backup location: "{local_backup_dir}"'
    ]))

    if not args.yes: prompt_proceed_exit("-> Ready to proceed? (y/n) ")

    print()
    install_new_ipykernel(kernel_name, display_name)
    backup_local(dest=local_backup_dir)
    set_userbase(kernel_name, local_backup_dir)
    install_launch_script(kernel_name)

    if args.yes or prompt_proceed("-> Remove python dependencies in ~/.local/lib? (y/n) "):
        remove_local()
        print("Python dependencies in ~/.local/lib are removed")
    print('Done')


def list_kernel(args):
    cmd = subprocess.run([
        'jupyter', 'kernelspec', 'list'
    ], capture_output=True)

    print(cmd.stdout.decode(), end='')


def remove_kernel(args):
    kernel_name = args.kernel_name
    if not kernel_exists(kernel_name):
        print(f'"{kernel_name}" does not exist', sys.stderr)
        sys.exit(1)

    # remove .local backup
    userbase_path = get_userbase(kernel_name)
    remove_dir(userbase_path)

    # remove kernelspec
    cmd = subprocess.run([
        'jupyter', 'kernelspec', 'remove', '-f', kernel_name
    ], capture_output=True)
    assert cmd.returncode == 0, cmd.stderr.decode()

    print('Done')


def get_parser():
    parser = argparse.ArgumentParser(
        prog='env-backup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='\n'.join([
            '----------',
            'env-activate, env-deactivate for switching between environments:',
            '  usage: source env-activate <KERNEL_NAME>',
            '         source env-deactivate',
            '  Manually verify by checking if `echo $PYTHONUSEBASE` is present'
        ])
    )

    subparsers = parser.add_subparsers(help='Commands to choose from')

    # Parser for command `new`
    parser_a = subparsers.add_parser('new', help='Create a new pip environment backup')
    parser_a.add_argument('--name', '-n', default=fmt_now(), help='Set name for new environment')
    parser_a.add_argument('--yes', '-y', action='store_true', help='automatically set every option to true')
    parser_a.set_defaults(func=new_kernel)

    # Parser for command `list`
    parser_b = subparsers.add_parser('list', help='List current environments (jupyter kernels)')
    parser_b.set_defaults(func=list_kernel)

    # Parser for command `remove`
    parser_c = subparsers.add_parser('remove', help='Remove envionment by name')
    parser_c.add_argument('kernel_name')
    parser_c.set_defaults(func=remove_kernel)

    return parser


def main():
    parser = get_parser()

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()