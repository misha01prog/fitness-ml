import ydb
import time

from app.logger import logger
from app.models import UserData, TrainData

driver_config = ydb.DriverConfig(
    'grpcs://ydb.serverless.yandexcloud.net:2135',
    '/ru-central1/b1gk8bp46725d6n4ve18/etn0c6gulrknr3mi0kck',
    credentials=ydb.credentials_from_env_variables(),
    root_certificates=ydb.load_ydb_root_certificate(),
)


def add_user_query(session, user: UserData):
    return session.transaction().execute(
        f'''INSERT INTO `users` (`id`,`age`,`sex`,`height`,`weight`,`fat`,`class`)
         VALUES (
         '{user.id}',
         {user.age},
         {user.sex},
         {user.height},
         {user.weight},
         {user.fat},
         {user.cls}
    )''',
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
    )


def get_user_query(session, user_id: str):
    return session.transaction().execute(
        f'''SELECT `id`, `age`,`class`,`fat`,`height`,`sex`,`weight`
        FROM users 
        WHERE `id`='{user_id}'
        LIMIT 1''',
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
    )


def add_train_query(session, train_data: TrainData):
    id_with_timestamp = f'{train_data.id}-{int(time.time())}'
    return session.transaction().execute(
        f'''INSERT INTO excersises (`id_with_time`,`id`,`pull_ups`,`push_ups`,`squats`,`sum_pullups`,`sum_pushups`,`sum_squats`)	
         VALUES (
         '{id_with_timestamp}',
         '{train_data.id}',
         {train_data.pull_ups},
         {train_data.push_ups},
         {train_data.squats},
         {train_data.sum_pullups},
         {train_data.sum_pushups},
         {train_data.sum_squats}
    )''',
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
    )


def get_last_train_query(session, user_id: str):
    return session.transaction().execute(
        f'''SELECT `id_with_time`,`id`,`pull_ups`,`push_ups`,`squats`,`sum_pullups`,`sum_pushups`,`sum_squats`
        FROM excersises 
        WHERE `id`='{user_id}'
        ORDER BY `id_with_time` DESC 
        LIMIT 1''',
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
    )


def save_user_to_db(user: UserData):
    logger.info("performing save user %s", user.id)
    with ydb.Driver(driver_config) as driver:
        try:
            driver.wait(timeout=8)
        except TimeoutError:
            logger.critical(
                f"connection failed\n" f"last reported errors by discovery: {driver.discovery_debug_details()}"
            )
            raise
        with ydb.SessionPool(driver, size=1, workers_threads_count=1) as pool:
            try:
                logger.info("performing add user query")
                pool.retry_operation_sync(add_user_query, ydb.RetrySettings(max_retries=2), user)
                logger.info("save user %s ok", user.id)
            except Exception as e:
                logger.critical(f"failed to create session pool due to {repr(e)}")
