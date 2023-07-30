from opet.api import OpetApiClient
import click


@click.command()
@click.option("--il", default="34", help="Yakıt fiyatlarını öğrenmek istediğiniz ilin plaka kodunu giriniz.")
def cli(il):
    client = OpetApiClient()
    try:
        print(client.price(il))
    except Exception as e:
        print(e)
