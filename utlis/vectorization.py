from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import config

authenticator = IAMAuthenticator(config.IBM_API_KEY)
nlu_service = NaturalLanguageUnderstandingV1(
    version='2023-08-01',
    authenticator=authenticator
)
nlu_service.set_service_url(config.IBM_SERVICE_URL)

def vectorize_query(query: str) -> list:
    try:
        response = nlu_service.analyze(
            text=query,
            features=Features(
                concepts=ConceptsOptions(limit=1)
            )
        ).get_result()

        vector = response.get('concepts', [{}])[0].get('relevance', [])

        if not vector:
            raise ValueError("Vector not found in the IBM Watson response")

        return vector
    except Exception as e:
        print(f"Error during vectorization: {e}")
        return []
