# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os
from datetime import timedelta
from typing import Optional, Dict
from superset.superset_typing import CacheConfig
from cachelib.file import FileSystemCache
from celery.schedules import crontab


logger = logging.getLogger()
def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL", "redis://redis:6379/0")
# Default cache for Superset objects
CACHE_CONFIG: CacheConfig = {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_PORT": "6379",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_KEY_PREFIX":"superset_13",
        "CACHE_REDIS_URL": CACHE_REDIS_URL
}

# Cache for datasource metadata and query results
DATA_CACHE_CONFIG: CacheConfig = {
        "CACHE_TYPE": "redis",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_REDIS_PORT": "6379",
        "CACHE_KEY_PREFIX":"superset_13_data",
        "CACHE_REDIS_URL": CACHE_REDIS_URL
}
FILTER_STATE_CACHE_CONFIG = {
        "CACHE_TYPE": "redis",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_REDIS_PORT": "6379",
        "CACHE_KEY_PREFIX":"superset_13_filter_state",
        "CACHE_REDIS_URL": CACHE_REDIS_URL
}
EXPLORE_FORM_DATA_CACHE_CONFIG = {
        "CACHE_TYPE": "redis",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_REDIS_PORT": "6379",
        "CACHE_KEY_PREFIX":"superset_13_explore_form",
        "CACHE_REDIS_URL": CACHE_REDIS_URL
}

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "1")

class CeleryConfig(object):
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("superset.sql_lab",)
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False
    CELERYBEAT_SCHEDULE = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {"ALERT_REPORTS": True, "DASHBOARD_CROSS_FILTERS": True, "DRILL_TO_DETAIL": True}


# Settings for Async Queries #
GLOBAL_ASYNC_QUERIES_REDIS_CONFIG = {
        "host": "redis",
        "port": "6379",
}

# UNCOMMENT AND ADD GLOBAL_ASYNC TO FEATURES FLAG TO ENABLE WS#
# GLOBAL_ASYNC_QUERIES_REDIS_STREAM_PREFIX = "async-events"
# GLOBAL_ASYNC_QUERIES_REDIS_STREAM_LIMIT = 1000
# GLOBAL_ASYNC_QUERIES_REDIS_STREAM_LIMIT_FIREHOSE = 1000000
# GLOBAL_ASYNC_QUERIES_JWT_COOKIE_NAME = "async-token"
# GLOBAL_ASYNC_QUERIES_JWT_COOKIE_SECURE = False
# GLOBAL_ASYNC_QUERIES_JWT_COOKIE_DOMAIN = None
# GLOBAL_ASYNC_QUERIES_JWT_SECRET = "alwfnbjigu19gfaovmb85fsalvdigesx"
# GLOBAL_ASYNC_QUERIES_TRANSPORT = "ws"
# GLOBAL_ASYNC_QUERIES_WEBSOCKET_URL = "ws://superset_websocket:8080/"
# GLOBAL_ASYNC_QUERIES_POLLING_DELAY = int(
#     timedelta(milliseconds=500).total_seconds() * 1000
# )



WTF_CSRF_ENABLED = False


ALERT_REPORTS_NOTIFICATION_DRY_RUN = False
# The base URL for the email report hyperlinks.
# False - reports will not works for real. True - email reports works.

SQLLAB_CTAS_NO_LIMIT = True
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "ru": {"flag": "ru", "name": "Russian"},
}


# UNCOMMECT FOR USING (Here's examples for setting up yandex reporter) # 
# SMTP_HOST = "smtp.yandex.com"
# SMTP_STARTTLS = False
# SMTP_SSL = True
# SMTP_SSL_SERVER_AUTH = True
# SMTP_USER = "any-user-name"
# SMTP_PORT = 465
# SMTP_PASSWORD = 'application-password'
# SMTP_MAIL_FROM = "email@yandex.ru"

# WEBDRIVER_BASEURL = "http://superset:8088"
# WEBDRIVER_BASEURL_USER_FRIENDLY="http://localhost:8088"

try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")