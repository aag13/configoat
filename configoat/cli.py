"""Console script for configoat."""
import click
from pathlib import Path
import sys
import shutil
from pkg_resources import resource_filename

@click.group()
def cli():
    pass

@cli.command()
def init():
    dir_name = click.prompt('Enter directory name', default='configs', type=str)
    file_name = click.prompt('Enter name of the main configuration file', default='main.yaml', type=str)
    click.echo("Configuration setup:")
    options = [
        "1. Single (Only one YAML file)",
        "2. Nested (Parent-child YAML files)",
        "3. Nested with Scripts (Includes .py scripts)"
    ]
    for option in options:
        click.echo("\t{}".format(option))

    choice = click.prompt("Select your setup choice", default=1, type=int)

    if dir_name.endswith("/"):
        dir_name = dir_name[:-1]

    if not (file_name.endswith(".yaml") or file_name.endswith(".yml")):
        file_name += ".yaml"

    if Path(dir_name).is_dir():
        click.echo("Folder '{}' already exists".format(dir_name))
        raise click.Abort()

    if choice not in [1, 2, 3]:
        click.echo("Invalid choice")
        raise click.Abort()

    templates_dir = resource_filename(__name__, "templates")

    try:
        if choice == 1:
            # create directory and copy only the main yaml file
            Path(dir_name).mkdir(parents=True)
            shutil.copy("{}/main.yaml".format(templates_dir), "{}/{}".format(dir_name, file_name))
        elif choice == 2:
            # create directory and copy both parent-child yaml files
            nested_yamls_dir = "{}/{}".format(dir_name, "yamls")

            Path(nested_yamls_dir).mkdir(parents=True)
            shutil.copy("{}/main_nested.yaml".format(templates_dir), "{}/{}".format(dir_name, file_name))
            shutil.copy("{}/nested.yaml".format(templates_dir), "{}/{}".format(nested_yamls_dir, "nested.yaml"))
        elif choice == 3:
            # create directory and copy parent-child yaml files and scripts folder
            nested_yamls_dir = "{}/{}".format(dir_name, "yamls")
            nested_scripts_dir = "{}/{}".format(dir_name, "scripts")

            Path(nested_yamls_dir).mkdir(parents=True)
            Path(nested_scripts_dir).mkdir(parents=True, exist_ok=True)
            shutil.copy("{}/main_nested_script.yaml".format(templates_dir), "{}/{}".format(dir_name, file_name))
            shutil.copy("{}/nested.yaml".format(templates_dir), "{}/{}".format(nested_yamls_dir, "nested.yaml"))
            shutil.copy("{}/script.py".format(templates_dir), "{}/{}".format(nested_scripts_dir, "script.py"))
    except:
        click.echo("Error during setup operation. Failed to cleanup")
    click.echo("Setup completed")


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
