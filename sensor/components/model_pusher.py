from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.predictor import ModelResolver
import os,sys
from sensor import utils
from sensor.predictor import ModelResolver

class ModelPusher:

    def __init__(self,model_pusher_config:config_entity.ModelPusherConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise SensorException(e, sys)

    
    def initiate_model_pusher(self):
        try:
            logging.info(f"Loading transformer model and target encoder")
            transformer=utils.load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model=utils.load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder=utils.load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            logging.info(f"Saving model into model pusher directory")
            utils.save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            utils.save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            utils.save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj=target_encoder)

            #saved model dir
            logging.info(f"Saving model in saved model dir")
            transformer_path=self.model_resolver.get_latest_save_transformer_path()
            model_path=self.model_resolver.get_latest_save_model_path()
            target_encoder_path=self.model_resolver.get_latest_save_target_encoder_path()

            utils.save_object(file_path=transformer_path, obj=transformer)
            utils.save_object(file_path=model_path, obj=model)
            utils.save_object(file_path=target_encoder_path, obj=target_encoder)


            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys)