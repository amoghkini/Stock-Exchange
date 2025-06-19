import click
import os
import sys
import socket

from instrument_registry.app.app import AppBuilder

app = AppBuilder().build('instrument_registry')


@click.group()
def cli():
    pass


@cli.command()
def run():
    """Run the Flask server if no other instance is using the port."""
    port = int(os.environ.get("PORT", 5000))

    if is_port_in_use(port):
        click.echo(f"❌ Port {port} is already in use. Is another instance running?")
        sys.exit(1)

    click.echo(f"✅ Starting server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port)


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


if __name__ == "__main__":
    cli()
