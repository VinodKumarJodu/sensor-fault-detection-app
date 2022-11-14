import os, sys
from sensor.logger import logging
from sensor.exceptions import SensorException
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.configurations.mongo_db_connection import MongoDBClient
from sensor.utils.main_utils import read_yaml_file, load_object
from sensor.constants.training_pipeline_constants import SAVED_MODEL_DIR
from sensor.constants.application import APP_HOST, APP_PORT
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping

from fastapi import FastAPI 
from fastapi.responses import Response 
from fastapi.middleware.cors import CORSMiddleware

from uvicorn import run as app_run
from starlette.responses import RedirectResponse

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainPipeline()
        if training_pipeline.is_pipeline_running:
            return Response("Training Pipeline is already running...!")
        training_pipeline.run_pipeline()
        return Response("Training Successful!") 
    except Exception as e:
        return Response(f"Error Occured! {e}")

@app.get("/predict")
async def predict_route():
    try:
        df = None
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df["predicted_column"] = y_pred 
        df["predicted_column"].replace(TargetValueMapping().reverse_mapping(), inplace=True)
    except Exception as e:
        raise Response(f"Error Occured..! {e}")
    



if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
    # try:
    #     training_pipeline = TrainPipeline()
    #     training_pipeline.run_pipeline()
    # except Exception as e:
    #     # logging.exception(e)
    #     raise e