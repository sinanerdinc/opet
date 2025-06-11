"""Command-line interface for fetching Opet fuel prices.

This module provides a CLI tool powered by Click to interact with the
OpetApiClient and display fuel price information for a specified province.
"""

from opet.api import OpetApiClient
from opet.exceptions import BaseError
import click
import sys


@click.command()
@click.option(
    "--il",
    "province_id",
    default=None,
    show_default=True,
    help=(
        "Enter the plate code of the province for which you want to "
        "learn fuel prices."
    ),
    metavar="PLATE_CODE"
)
@click.option(
    "--api",
    is_flag=True,
    help="Start the API server instead of running the CLI."
)
def cli(province_id: str, api: bool) -> None:
    """Starts the API server."""
    if api:
        import uvicorn
        uvicorn.run("opet.server.app:app", host="0.0.0.0", port=8000)
        return
    if province_id is None:
        click.echo(
            "use the --help command to see the available options",
            err=True
        )
        sys.exit(1)
    try:
        client = OpetApiClient()
        price_json_output: str = client.price(province_id)
        click.echo(price_json_output)
    except BaseError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
