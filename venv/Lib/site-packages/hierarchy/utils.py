import click


class Config:
    __instance = None

    verbose = False

    @staticmethod
    def get_instance() -> 'Config':
        if Config.__instance is None:
            Config()

        return Config.__instance

    def __init__(self):
        if Config.__instance is not None:
            raise Exception("This class is a singleton! Use 'get_instance()")

        Config.__instance = self


def display(text, variant=None, reason=None):
    if not variant:
        click.echo(text)
        return

    if variant == 'ERROR':
        click.echo(text, err=True)
        if Config.get_instance().verbose and reason is not None:
            click.echo(str(reason), err=True)
        return
