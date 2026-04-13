import typer

app = typer.Typer()

@app.command()
def run():
    typer.echo("Shader I18n CLI")

if __name__ == "__main__":
    app()