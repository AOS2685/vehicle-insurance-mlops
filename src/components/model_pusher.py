import sys 
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.s3_estimator import Proj1Estimator

class ModelPusher:
    def __init__(
        self, 
        model_evaluation_artifact: ModelEvaluationArtifact,
        model_pusher_config: ModelPusherConfig
    ):
        """
        :param model_evaluation_artifact: Output reference of model evaluation artifact stage
        :param model_pusher_config: Config for model pusher
        """
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        
        # Initialize the S3-backed estimator
        self.proj1_estimator = Proj1Estimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path
        )
    
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Pushes the trained model to the S3 bucket.

        Returns:
            ModelPusherArtifact: Artifact containing S3 bucket info
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            logging.info("----------------------")
            logging.info("Uploading artifacts folder to S3 bucket")
            logging.info("Uploading new model to S3 bucket....")

            # Upload model using Proj1Estimator
            self.proj1_estimator.save_model(
                from_file=self.model_evaluation_artifact.trained_model_path,
                remove=False  # keep local copy if needed
            )

            # Create artifact for logging/tracking
            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path
            )
            
            logging.info("Uploaded artifacts folder to S3 bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")

            return model_pusher_artifact

        except Exception as e:
            raise MyException(e, sys) from e



# import sys 
# from src.cloud_storage.aws_storage import SimpleStorageService
# from src.exception import MyException
# from src.logger import logging
# from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
# from src.entity.config_entity import ModelPusherConfig
# from src.entity.s3_estimator import Proj1Estimator

# class ModelPusher:
#     def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
#                     model_pusher_config: ModelPusherConfig
#                  ):
#         """
#             :param model_evaluation_artifact: Output reference of data evaluation artifact stage
#             :param model_pusher_config: Config for model pusher
#         """
#         self.s3 = SimpleStorageService()
#         self.model_evaluation_artifact = model_evaluation_artifact
#         self.model_pusher_config = model_pusher_config
#         self.proj1_estimator = Proj1Estimator(
#             bucket_name = model_pusher_config.bucket_name,
#             model_path=model_pusher_config.s3_model_key_path
#         )
    
#     def initiate_model_pusher(self) -> ModelPusherArtifact:
#         """
#             Method Name : initiate_model_evaluation
#             Description: This function is used to initiate all steps of the model pusher

#             Output : Returns model evaluation artifact
#             On Failure : Write an exception log and then raise an exception
#         """
#         logging.info("Entered initiate_model_pusher method of ModelTrainer class")

#         try:
#             print("----------------------")
#             logging.info("Uploading artifacts folder to s3 bucket")
#             logging.info("Uploading new model to s3 bucket....")
#             self.proj1_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
#             model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
#                                                         s3_model_path=self.model_pusher_config.s3_model_key_path
#                                                         )
            
#             logging.info("Uploaded artifacts folder to s3 bucket")
#             logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
#             logging.info("Exited initiate_model_pusher method of ModelTrainer class")

#             return model_pusher_artifact
#         except Exception as e:
#             raise MyException(e,sys) from e