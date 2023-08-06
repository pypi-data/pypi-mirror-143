import click
from pathlib import Path
import os
import yaml
import sentry_sdk
from sentry_sdk import capture_exception
import sys

from ocean import code
from ocean.utils import sprint, PrintType, version_check

if "OC_DEBUG" not in os.environ.keys():
    sentry_sdk.init(
        "https://a6b6c48c3f444b9f99ca70b543c09a46@o922093.ingest.sentry.io/5881410",
        traces_sample_rate=0.1,
        environment="production",
        release=f"ocean-cli@{code.VERSION}",
        send_default_pii=True,
    )


class Environment:
    def __init__(self, load=True):
        self.verbose = False
        self.config_path = Path.home() / ".ocean" / "config.yaml"
        self.config = {}

        if load:
            self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            sprint(f"Config file '{self.config_path}' is not exist.", PrintType.FAILED)
            sprint("Please run:\n\n\tocean init\n")
            exit()

        with open(self.config_path, "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def save_config(self):
        with open(self.config_path, "w") as f:
            yaml.dump(self.config, f)

    def update_config(self, key, value):
        self.config.update({key: value})
        self.save_config()

    def get_auth_token(self):
        return self.config.get(code.AUTH_TOKEN)

    def get_url(self):
        return self.config.get(code.OCEAN_URL)

    def get_token(self):
        return self.config.get(code.TOKEN)

    def get_username(self):
        return self.config.get(code.USERNAME)

    def get_email(self):
        return self.config.get(code.EMAIL)

    # preset
    def get_presets(self):
        return self.config[code.PRESETS]

    def add_preset(self, preset):
        if self.preset_exist(preset[code.NAME]):
            sprint(f"Preset `{preset[code.NAME]}` is already exist.", PrintType.FAILED)
            return
        if preset[code.DEFAULT]:
            for p in self.config[code.PRESETS]:
                p[code.DEFAULT] = False
        self.config[code.PRESETS].append(preset)
        self.save_config()

    def delete_presets(self, key):
        for idx, pre in enumerate(self.config[code.PRESETS]):
            if pre["name"] == key:
                del self.config[code.PRESETS][idx]
                self.save_config()
                break
        else:
            sprint(f"Preset `{key}` not found.", PrintType.FAILED)
            exit()

    def set_presets_as_default(self, preset_name):
        if not self.preset_exist(preset_name):
            sprint(f"Preset `{preset_name}` is not exist.", PrintType.FAILED)
            return
        for p in self.config[code.PRESETS]:
            if p[code.NAME] == preset_name:
                p[code.DEFAULT] = True
            else:
                p[code.DEFAULT] = False
        self.save_config()
        sprint(f"Preset `{preset_name}` is now default.", PrintType.SUCCESS)

    def preset_exist(self, name):
        for p in self.config[code.PRESETS]:
            if p[code.NAME] == name:
                return True
        return False

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        sprint(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_env = click.make_pass_decorator(Environment, ensure=True)

CONTEXT_SETTINGS = dict(auto_envvar_prefix="COMPLEX")
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"ocean.commands.cmd_{name}", None, None, ["cli"])
        except ImportError as e:
            sprint(e)
            return
        return mod.cli


@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
def cli():
    is_latest, latest, current = version_check()
    if not is_latest:
        sprint(
            f" New version({latest}) of Ocean-cli released. Please upgrade ocean-cli. (current: {current})",
            PrintType.WORNING,
        )
    pass


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        sprint("Unknown Error Occured.", PrintType.FAILED)
        capture_exception(e)
