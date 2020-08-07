## Python Local Environment Backup Tool

### What is this
Because of file permission issues, DataHub/DSMLP can only install python pip packages under the user space (`~/.local/`). The advantage is that packages can persist between uses. This command-line utility will allow you to create and customize jupyter kernels that can be used in jupyter environments. You will be able to switch between envionments by selecting the appropriate kernel when creating the notebook or by switching to it inside the notebook interface dropdown menu under "Kernel" -> "Change kernel".

### Use cases
- You have two projects that require different sets of pip packages and they are causing compatibility issues
- You want a clean starting ground for a new project but also would like to backup the old environment

### What it does
- Creates a backup of the current environment in `~/.local` under `~/.local_backups`
- Creates a custom kernel that can activate the backed-up envionment
- (Optional) Deletes all the installed site-packages under `~/.local/lib`
- You need to refresh the web page to see the newly created kernel

### Usage
```
env-backup [-h] {new,list,remove} ...

Arguments:
 -  list             List current environments (jupyter kernels)
 -  new              Create a new pip environment backup
        optional arguments:
          --name NAME, -n NAME  Set name for new environment
          --yes, -y             automatically set every option to true

 -  remove           Remove envionment by name
        positional arguments:
          kernel_name,          Kernel (environment) name to be deleted



source env-activate <kernel_name>
source env-deactivate
```

### Q&A
- #### How do I use the backed-up environment outside jupyter notebooks (e.g. in a terminal)?


1. Inside a jupyter notebook with the desired kernel, run `import os; print(os.environ['PYTHONUSERBASE'])`.
2. Inside a terminal, run `export PYTHONUSERBASE='LOCAL_ENV_BACKUP_DIR'` where `LOCAL_ENV_BACKUP_DIR` is the output from step 1.
3. In the same terminal, run your python script.

Alternatively, you can use `source env-activate <kernel_name>` and `source env-deactivate` for changing python environments.
