from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from services.ssm_store import get_parameter

PERSONAL_ACCESS_TOKEN = get_parameter("PERSONAL_ACCESS_TOKEN")
USER_ID = "aligulzar"
APP_ID = "recipe-ai"
MODEL_ID = "food-item-recognition"
MODEL_VERSION_ID = "1d5fd481e0cf4826aa72ec3ff049e044"


def infer_ingredient(image_url: str):
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID),
            model_id=MODEL_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(image=resources_pb2.Image(url=image_url))
                )
            ],
        ),
        metadata=(("authorization", "Key " + PERSONAL_ACCESS_TOKEN),),
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception(
            "Post model outputs failed, status: "
            + post_model_outputs_response.status.description
        )

    output = post_model_outputs_response.outputs[0]
    return output.data.concepts[0].name
