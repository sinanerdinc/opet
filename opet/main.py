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
    default="34",
    show_default=True,
    help=(
        "Yakıt fiyatlarını öğrenmek istediğiniz ilin plaka kodunu giriniz."
    ),
    metavar="PLAKA_KODU"
)
def cli(province_id: str) -> None:
    """Fetches and displays Opet fuel prices for the specified province ID.

    This tool initializes an OpetApiClient and calls its price method
    to retrieve and print fuel price data in JSON format.
    Error messages are printed to stderr if issues occur.

    Args:
        province_id: The plate code (plaka kodu) of the province for which
                     to fetch fuel prices.
    """
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
