"""Command-line interface for fetching Opet fuel prices.

This module provides a CLI tool powered by Click to interact with the OpetApiClient
and display fuel price information for a specified province.
"""

from opet.api import OpetApiClient
from opet.exceptions import BaseError # Catching BaseError for application-specific errors
import click
import os # For API Key, though not used by current OpetApiClient
import sys # For exiting with error code

@click.command()
@click.option(
    "--il",
    "province_id", # Use a more descriptive variable name internally
    default="34",
    show_default=True, # Makes default visible in --help
    help="Yakıt fiyatlarını öğrenmek istediğiniz ilin plaka kodunu giriniz.",
    metavar="PLAKA_KODU" # Adds context in help message
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
    # Example of how an API key might be handled if needed in the future.
    # Not currently used by OpetApiClient as per its latest implementation.
    # api_key = os.environ.get("OPET_API_KEY")
    # if not api_key:
    #     click.echo("Error: OPET_API_KEY environment variable not set.", err=True)
    #     sys.exit(1)

    try:
        # Pass api_key to client if it were to accept it:
        # client = OpetApiClient(api_key=api_key)
        client = OpetApiClient()
        price_json_output: str = client.price(province_id)
        click.echo(price_json_output)
    except BaseError as e: # Catching specific application errors
        click.echo(f"Error: {e}", err=True)
        sys.exit(1) # Exit with a non-zero status code for application errors
    except Exception as e: # Catch unexpected errors
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1) # Exit with a non-zero status code for unexpected errors

if __name__ == '__main__':
    cli()
