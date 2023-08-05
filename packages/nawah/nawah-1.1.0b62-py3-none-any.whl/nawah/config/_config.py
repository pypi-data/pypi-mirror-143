from typing import (TYPE_CHECKING, Any, Callable, Dict, List, Optional, Set,
                    Union)

from nawah.enums import LOCALE_STRATEGY

if TYPE_CHECKING:
    from datetime import datetime

    import redis.commands.json.JSON
    from bson import ObjectId
    from motor.motor_asyncio import AsyncIOMotorClient

    from nawah.base_module import BaseModule
    from nawah.classes import (ANALYTICS_EVENTS, ATTR, CLIENT_APP, JOB,
                               NAWAH_DOC, NAWAH_ENV, SYS_DOC, USER_SETTING)


class Config:
    debug: bool = False
    env: str
    port: int = 8081

    _sys_conn: 'AsyncIOMotorClient'
    _sys_cache: Optional['redis.commands.json.JSON'] = None
    _sys_env: 'NAWAH_ENV'
    _sys_docs: Dict['ObjectId', 'SYS_DOC'] = {}
    _jobs_base: 'datetime'

    _nawah_version: str
    packages_api_levels: Dict[str, str] = {}
    packages_versions: Dict[str, str] = {}

    _app_name: str
    _app_version: str
    _app_default_package: str
    _app_path: str
    _app_packages: Dict[str, str]

    test: bool = False

    emulate_test: bool = False
    force_admin_check: bool = False

    generate_ref: bool = False
    _api_ref: str

    generate_models: bool = False
    _api_models: str

    vars_types: Dict[str, Union['ATTR', Dict[str, Any]]] = {}
    vars: Dict[str, Any] = {}

    client_apps: Dict[str, 'CLIENT_APP'] = {}

    analytics_events: 'ANALYTICS_EVENTS' = {
        'app_conn_verified': True,
        'session_conn_auth': True,
        'session_user_auth': True,
        'session_conn_reauth': True,
        'session_user_reauth': True,
        'session_conn_deauth': True,
        'session_user_deauth': True,
    }

    conn_timeout: int = 120
    quota_anon_min: int = 40
    quota_auth_min: int = 100
    quota_ip_min: int = 500
    file_upload_limit: int = -1
    file_upload_timeout: int = 300

    data_server: str = 'mongodb://localhost'
    data_name: str = 'nawah_data'
    data_ssl: bool = False
    data_ca_name: Optional[str] = None
    data_ca: Optional[str] = None
    data_disk_use: bool = False

    data_azure_mongo: bool = False

    cache_server: Optional[str] = None
    cache_db: Optional[int] = 0
    cache_username: Optional[str] = None
    cache_password: Optional[str] = None
    cache_expiry: Optional[int] = None
    _cache_channels: Set[str] = set()

    locales: List[str] = ['ar_AE', 'en_AE']
    locale: str = 'ar_AE'
    locale_strategy: 'LOCALE_STRATEGY' = LOCALE_STRATEGY.DUPLICATE

    admin_doc: 'NAWAH_DOC' = {}
    admin_password: str = '__0xADMIN'

    anon_token: str = '__ANON_TOKEN_f00000000000000000000012'
    anon_privileges: Dict[str, List[str]] = {}

    user_attrs: Dict[str, 'ATTR'] = {}
    user_settings: Dict[str, 'USER_SETTING'] = {}
    user_doc_settings: List[str] = []

    groups: List[Dict[str, Any]] = []
    default_privileges: Dict[str, List[str]] = {}

    data_indexes: List[Dict[str, Any]] = []

    docs: List['SYS_DOC'] = []

    l10n: Dict[str, Dict[str, Any]] = {}

    jobs: Dict[str, 'JOB'] = {}

    gateways: Dict[str, Callable] = {}

    types: Dict[str, Callable] = {}

    modules: Dict[str, 'BaseModule'] = {}
    modules_packages: Dict[str, List[str]] = {}
