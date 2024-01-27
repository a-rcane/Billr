from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['configs/settings.yaml', 'configs/.secrets.yaml'],

    environments=True,

    load_dotenv={"when": {"env": {"is_in": ["development"]}}},

    env_switcher="ENV_FOR_DYNACONF",
    dotenv_path="configs.env"
)