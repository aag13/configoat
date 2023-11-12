"""Console script for pyenvconfig."""
import click
import os
import sys

@click.group()
def cli():
    pass

@cli.command()
@click.argument('dir_name')
@click.argument('file_name')
def init(dir_name, file_name):
    # Create the directory
    if os.path.exists(dir_name):
        sys.exit("{} already exists".format(dir_name))
    os.mkdir(dir_name)

    # Create the YAML file inside the directory
    yaml_file_path = os.path.join(dir_name, f"{file_name}.yaml")
    if not os.path.exists(yaml_file_path):
        with open(yaml_file_path, 'w') as f:
            f.write("# Your YAML content goes here")

    click.echo("Created {}/{}.yaml".format(dir_name, file_name))


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
