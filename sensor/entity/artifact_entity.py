from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    tranform_object_path:str
    tranformed_train_path:str
    tranformed_test_path:str

class ModelTrainerArtifact:
    pass

class ModelEvaluationArtifact:
    pass

class ModelPusherArtifact:
    pass