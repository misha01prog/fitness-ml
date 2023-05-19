import joblib
import sklearn  # noqa (for correct model importing)
import ydb
from fastapi import BackgroundTasks, FastAPI, HTTPException

from app.db import save_user_to_db, driver_config, get_user_query, add_train_query, get_last_train_query
from app.logger import logger
from app.models import UserData, ScoreResponse, TrainData
from app.motivation import MotivationEngine

app = FastAPI(
    title="Machine learning server",
)
model = None


@app.on_event("startup")
async def startup_event():
    global model
    with open("ml/model.pkl", 'rb') as m:
        model = joblib.load(m)
        logger.debug("loaded model %s", model)


@app.get("/get/{user_id}", description="получает данные пользователя")
async def get(user_id: str):
    with ydb.Driver(driver_config) as driver:
        try:
            logger.info("connecting to the database")
            driver.wait(timeout=8)
        except TimeoutError:
            logger.critical(
                f"connection failed\n" f"last reported errors by discovery: {driver.discovery_debug_details()}"
            )
            raise
        with ydb.SessionPool(driver, size=1, workers_threads_count=1) as pool:
            try:
                logger.info("performing get query")
                result = pool.retry_operation_sync(get_user_query, ydb.RetrySettings(max_retries=2), user_id)
                if result[0].rows is None:
                    raise HTTPException(status_code=404, detail="User not found")
                else:
                    data = result[0].rows[0]
                    return UserData(
                        id=user_id,
                        age=data['age'],
                        sex=data['sex'],
                        height=data['height'],
                        weight=data['weight'],
                        fat=data['fat'],
                        cls=data['class']
                    )
            except Exception as e:
                logger.critical(f"failed to create session pool due to {repr(e)}")
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/score", description="добавляет пользователя в бд и предсказывает для него оптимальное кол-во упражнений")
async def score(payload: UserData, background_tasks: BackgroundTasks):
    background_tasks.add_task(save_user_to_db, payload)

    predicted = model.predict(payload.to_dataframe())[0]
    pushups, pullups, squats = int(predicted[0]), int(predicted[1]), int(predicted[2])
    if payload.sex == 2:
        pullups = 0
    logger.info(f"predicted {pushups} push_ups ; {pullups} pull_ups ; {squats} squats for {payload.json()}")
    return ScoreResponse(pushups=pushups, pullups=pullups, squats=squats)


@app.post("/train", description="добавляет тренировку пользователя")
async def train(current_train: TrainData):
    logger.info("performing save train %s", current_train.json())
    last_train = None
    with ydb.Driver(driver_config) as driver:
        try:
            logger.info("connecting to the database")
            driver.wait(timeout=8)
        except TimeoutError:
            logger.critical(
                f"connection failed\n" f"last reported errors by discovery: {driver.discovery_debug_details()}"
            )
            raise
        with ydb.SessionPool(driver, size=1, workers_threads_count=1) as pool:
            try:
                logger.info("performing get last train query")
                last_train_query_result = pool.retry_operation_sync(get_last_train_query,
                                                                    ydb.RetrySettings(max_retries=2), current_train.id)
                if len(last_train_query_result[0].rows) != 0:
                    res = last_train_query_result[0].rows[0]
                    logger.info("found last train %s", res)
                    last_train = TrainData(
                        id=res['id'],
                        pull_ups=res['pull_ups'],
                        push_ups=res['push_ups'],
                        squats=res['squats'],
                        sum_pullups=res['sum_pullups'],
                        sum_pushups=res['sum_pushups'],
                        sum_squats=res['sum_squats']
                    )
                else:
                    logger.info("not found last train")
                logger.info("performing add train query")
                pool.retry_operation_sync(add_train_query, ydb.RetrySettings(max_retries=2), current_train)
                logger.info("save train %s ok", current_train.id)
            except Exception as e:
                logger.critical(f"failed to create session pool due to {repr(e)}")

        motivation = MotivationEngine(last_train, current_train).summarize() if last_train is not None else []
        return {'motivation': motivation}

    #  получаем предыдущий результат (если есть)
