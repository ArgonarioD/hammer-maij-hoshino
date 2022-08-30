from httpx import Response


def get_json_data_from_response(response: Response) -> dict:
    return response.json()['data']
