import requests
import logging
from time import sleep
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self):
        """
        Initialize the LLMService with API URL and API key.
        """
        self.api_url = os.getenv("LLM_API_URL")
        self.api_key = os.getenv("LLM_API_KEY")
        self.max_retries = 3
        self.timeout = 10

    def generate_recommendations(self, vehicle_details):
        """
        Sends vehicle details to the LLM API and gets back practical recommendations.

        Args:
            vehicle_details (dict): Dictionary containing vehicle attributes.

        Returns:
            dict: Response from the LLM API containing recommendations or error message.
        """
        
        payload = self._construct_payload(vehicle_details)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }


        for attempt in range(self.max_retries):
            try:
                # Make API request with timeout and retry mechanism
                response = requests.post(self.api_url, json=payload, headers=headers, timeout=self.timeout)

                if response.status_code == 200:
                    return response.json()
                else:
                    logging.error(f"LLM API failed with status code {response.status_code}: {response.text}")
                    return {"error": f"LLM API call failed with status {response.status_code}: {response.text}"}
            
            except requests.exceptions.Timeout:
                logging.warning(f"Request timed out (Attempt {attempt + 1}/{self.max_retries}). Retrying...")
                sleep(2)  # Wait before retrying
            except requests.exceptions.RequestException as e:
                logging.error(f"An error occurred: {e}")
                return {"error": f"Request failed with error: {e}"}
        
        return {"error": "Max retries reached. Could not get a response from LLM API."}

    def _construct_payload(self, vehicle_details):
        """
        Constructs the payload to send to the LLM API, including vehicle details.

        Args:
            vehicle_details (dict): The details of the vehicle.

        Returns:
            dict: The formatted payload for the API request.
        """
        return {
            "model": "llama-3.3-70b-versatile",
            "messages": [{
                "role": "user",
                "content": (
                    f"Based on the vehicle details provided, suggest practical ways to reduce CO2 emissions "
                    f"and improve fuel economy. Avoid costly solutions like buying new vehicles. "
                    f"Vehicle details:\n"
                    f"Model: {vehicle_details.get('model', 'N/A')}\n"
                    f"Transmission: {vehicle_details.get('Transmission', 'N/A')}\n"
                    f"Type: {vehicle_details.get('Vehicle_Type', 'N/A')}\n"
                    f"Engine: {vehicle_details.get('Engine_Capacity', 'N/A')}L, {vehicle_details.get('Engine_Power', 'N/A')} PS\n"
                    f"Fuel: {vehicle_details.get('Fuel_Type', 'N/A')}\n"
                    f"Powertrain: {vehicle_details.get('Powertrain', 'N/A')}\n"
                    f"CO2 Emission: {vehicle_details.get('CO2_Emission', 'N/A')} g/km"
                )
            }]
        }
