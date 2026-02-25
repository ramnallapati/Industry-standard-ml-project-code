import os
import sys
import mlflow
import mlflow.sklearn

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_model
)
from networksecurity.utils.ml_utils.metric.classification_metric import (
    get_classification_score
)

# ML Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)


class ModelTrainer:

    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    # ==========================
    # MLflow Tracking
    # ==========================
    def track_mlflow(self, best_model, train_metric, test_metric):

        mlflow.set_experiment("NetworkSecurityExperiment")

        with mlflow.start_run():

            # Log model name
            mlflow.log_param("model_name", type(best_model).__name__)

            # Log Train Metrics
            mlflow.log_metric("train_f1_score", train_metric.f1_score)
            mlflow.log_metric("train_precision", train_metric.precision_score)
            mlflow.log_metric("train_recall", train_metric.recall_score)

            # Log Test Metrics
            mlflow.log_metric("test_f1_score", test_metric.f1_score)
            mlflow.log_metric("test_precision", test_metric.precision_score)
            mlflow.log_metric("test_recall", test_metric.recall_score)

            # Log model artifact
            mlflow.sklearn.log_model(best_model, name="model")

    # ==========================
    # Train Model
    # ==========================
    def train_model(self, x_train, y_train, x_test, y_test):

        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=0),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "AdaBoost": AdaBoostClassifier()
            }

            params = {
                "Random Forest": {
                    'n_estimators': [16, 32, 64]
                },
                "Decision Tree": {
                    'criterion': ['gini', 'entropy']
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01],
                    'n_estimators': [16, 32]
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    'learning_rate': [0.1, 0.01],
                    'n_estimators': [16, 32]
                },
            }

            # Evaluate all models
            model_report: dict = evaluate_model(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
                models=models,
                params=params
            )

            # Select best model
            best_model_score = max(model_report.values())
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            logging.info(f"Best Model: {best_model_name}")
            logging.info(f"Best Score: {best_model_score}")

            # Predictions
            y_train_pred = best_model.predict(x_train)
            y_test_pred = best_model.predict(x_test)

            # Metrics
            classification_train_metric = get_classification_score(
                y_true=y_train,
                y_pred=y_train_pred
            )

            classification_test_metric = get_classification_score(
                y_true=y_test,
                y_pred=y_test_pred
            )

            # Load Preprocessor
            preprocessor = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )

            # Wrap model with preprocessor
            network_model = NetworkModel(
                preprocessor=preprocessor,
                model=best_model
            )

            # Save Model
            os.makedirs(
                os.path.dirname(self.model_trainer_config.trained_model_file_path),
                exist_ok=True
            )

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=network_model
            )

            # Track MLflow (single run)
            self.track_mlflow(
                best_model,
                classification_train_metric,
                classification_test_metric
            )

            # Create artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    # ==========================
    # Initiate Model Trainer
    # ==========================
    def initiate_model_trainer(self) -> ModelTrainerArtifact:

        try:
            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )

            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact = self.train_model(
                x_train, y_train, x_test, y_test
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e