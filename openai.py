import orjson
from retry import retry
from ai_tools.openai.constants import OpenAI
from ai_tools.openai.endpoints import Endpoints
from utils.decorators import typecheck
from exceptions import RequestFailed, InvalidResponse, ModelNotFound

class Model(OpenAI, Endpoints):

    @typecheck(object, str)
    def set_model_name(self, model_name: str):
        """Sets the model name used for this OpenAI tool

        Args:
            model_name (str): Your model name (gpt-4, gpt-3.5-turbo, ...)
        """
        self.model_name = model_name

    def get_model_name(self) -> str:
        """Return model name

        Returns:
            str: Model name
        """
        return self.model_name
    
    @retry(RequestFailed, tries=OpenAI.max_retries(), delay=OpenAI.retry_delay())
    def retrieve_model(self) -> tuple[str, int, str]:
        """Get model data (and check if it exists)

        Raises:
            RequestFailed: The request to OpenAI server failed
            InvalidResponse: The response cannot be read directly due to format errors.
            ModelNotFound: The specified model cannot be found

        Returns:
            tuple[str, int, str]: Model ID, Model Creation Time, Model Owner
        """
        model_name: str = self.get_model_name()

        try:
            response = self.session.get(
                url=self.RETRIEVE_MODEL_ENDPOINT.format(model_name=model_name),
                headers={
                    'Authorization': f'Bearer {self.API_KEY}'
                }
            )
        except:
            raise RequestFailed('Model retrieving has failed due to connection errors.')
        
        try:
            response_json = orjson.loads(response.text)
        except:
            raise InvalidResponse('Model retrieving has failed due to incorrect response format.')
        
        response_model_id: str = response_json.get('id', None)
        response_model_created_time: int = response_json.get('created', None)
        response_model_owned_by: str = response_json.get('owned_by', None)

        if not any([response_model_id, response_model_created_time, response_model_owned_by]):
            raise ModelNotFound(f'Model {model_name} does not exist on OpenAI database.')

        return response_model_id, \
        response_model_created_time, \
        response_model_owned_by
