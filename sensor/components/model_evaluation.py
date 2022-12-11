from sensor.predictor import ModelResolver
from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import sys,os
from sensor import utils
from sklearn.metrics import f1_score
import pandas as pd

class ModelEvaluation:

    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact      
        ):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise SensorException(e,sys)



    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            #if saved model folder has model the we will compare 
            #which model is best trained or the model from saved model folder

            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact

            transformer_path=self.model_resolver.get_latest_transformer_path()       
            model_path=self.model_resolver.get_latest_model_path()
            target_encoder_path=self.model_resolver.get_latest_target_encoder_path()


            transformer=utils.load_object(file_path=transformer_path)
            model=utils.load_object(file_path=model_path)
            target_encoder=utils.load_object(file_path=target_encoder_path)


            current_transformer=utils.load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model=utils.load_object(file_path=self.data_transformation_artifact.model_path)
            current_target_encoder=utils.load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            test_df=pd.DataFrame(self.data_ingestion_artifact.test_file_path)
            target_df=test_df[test_df]
            #Accuracy
            input_arr=transformer.transform(test_df)


        except Exception as e:
            raise SensorException(e,sys)
