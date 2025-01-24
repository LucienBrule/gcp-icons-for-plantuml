import click
from pathlib import Path

from . import env, builder, configgen, fetcher

@click.group()
def cli():
    """GCP Icons for PlantUML."""
    pass

@cli.command()
def check_env():
    """Check environment prerequisites."""
    env.verify()

@cli.command()
def create_config_template():
    """Create a config-template.yml based on current icons."""
    configgen.create()

@cli.command()
def build():
    """Build icons and generate PlantUML files."""
    builder.build_all()

@cli.command()
def fetch_icons():
    """
    Download the GCP basic-cards zip,
    unzip, normalize, and copy into source/official.
    """
    fetcher.fetch_and_prepare_icons()

@cli.command()
@click.option("--grid-size", default=5, help="Size of the N x N grid (default is 5).")
@click.option("--output-dir", default="benchmark", help="Directory to save the generated .puml file.")
def generate_kitchen_sink(grid_size, output_dir):
    """
    Generate a kitchen-sync example with an NxN grid of icons.
    """
    from .kitchen_sink import generate_kitchen_sync_example
    generate_kitchen_sync_example(grid_size, output_dir)

@cli.command()
@click.option("--output-dir", default="benchmark/verification", help="Directory to save the verification .puml files.")
def generate_verification_examples(output_dir):
    """
    Generate verification .puml files for each individual icon.
    """
    from .kitchen_sink import generate_verification_examples
    generate_verification_examples(output_dir)

@cli.command()
@click.option("--output-dir", default="benchmark", help="Directory to save the benchmark .puml file.")
@click.option("--num-nodes", default=100, help="Number of nodes in the diagram (default: 100).")
@click.option("--max-connections", default=5, help="Maximum connections per node (default: 5).")
def generate_complex_diagram(output_dir, num_nodes, max_connections):
    """
    Generate a complex network diagram with interconnected icons.
    """
    from .kitchen_sink import generate_complex_diagram
    generate_complex_diagram(output_dir, max_connections, num_nodes)