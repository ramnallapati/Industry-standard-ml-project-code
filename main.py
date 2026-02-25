
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
import os
import sys
import pymongo


if __name__ == "__main__":
  try:
    trainingpipelineconfig = TrainingPipelineConfig()
    dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
    data_ingestion = DataIngestion(dataingestionconfig)
    logging.info("Initiate the Data ingestion")
    dataingestionartifact = data_ingestion.initiate_data_ingestion()
    logging.info("Data Ingestion completed")
    print(dataingestionartifact)
    datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
    data_validation = DataValidation(dataingestionartifact,datavalidationconfig)
    logging.info("Initiate Data validation")
    data_validation_artifact = data_validation.initiate_data_validation()
    logging.info("data validation completed")
    print(data_validation_artifact)
    logging.info("Data Transformation Initiatiated")
    datatransformationconfig = DataTransformationConfig(trainingpipelineconfig)
    datatransformation = DataTransformation(data_validation_artifact,datatransformationconfig)
    datatransformationartifact = datatransformation.initiate_data_transformation()
    print(datatransformationartifact)
    logging.info("Data Transformation Completed")
  except Exception as e:
    raise NetworkSecurityException(e,sys)