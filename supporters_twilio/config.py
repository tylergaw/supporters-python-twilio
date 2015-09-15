import logging.config
import os


class DevConfig(object):
    DEBUG = False
    LOGGING_LEVEL = logging.INFO
    TESTING = False


class ProdConfig(object):
    DEBUG = False
    LOGGING_LEVEL = logging.WARNING
    TESTING = False


class LocalConfig(object):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG
    TESTING = False


class TestConfig(object):
    DEBUG = False
    LOGGING_LEVEL = logging.INFO
    TESTING = True


def _config_logger(app):
    """
    Configure the application's logger

    :param Flask instance
    """
    level = app.config['LOGGING_LEVEL']

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': ('%(asctime)s - %(name)s - %(process)d -'
                           ' %(levelname)s - %(message)s'),
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {},
        'root': {
            'handlers': ['default'],
            'level': level,
        },
    }
    logging.config.dictConfig(LOGGING)

def config_app(app, env):
    configs = {
        'local': LocalConfig,
        'dev': DevConfig,
        'prod': ProdConfig,
        'test': TestConfig,
    }

    if env in configs:
        app.config.from_object(configs[env]())

    else:
        reason = '"{}" is not a valid ENV. Try one of: "{}"'.format(
            env,
            '", "'.join(list(configs.keys())))
        raise KeyError(reason)

    _config_logger(app)
