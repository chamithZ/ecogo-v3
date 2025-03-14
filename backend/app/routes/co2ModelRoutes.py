from flask import Blueprint, request, jsonify
from models.co2_prediction import inference_co2, model_co2, encoder_co2
from app.services.vehicleService import VehicleService

co2_bp = Blueprint('co2', __name__)

@co2_bp.route('/predict', methods=['POST'])
def predict():
    """
    Handle POST requests for single vehicle CO₂ emission prediction.
    """
    try:
        if model_co2 is None or encoder_co2 is None:
            return jsonify({'error': 'Model or encoder not loaded'}), 500

        input_data = request.get_json()
        if not input_data:
            return jsonify({'error': 'No input data provided'}), 400

        vehicle_id = input_data.pop('vehicle_id', None)  # Remove vehicle_id before inference
        if not vehicle_id:
            return jsonify({'error': 'Vehicle ID is required'}), 400

        # Predict CO₂ emission
        prediction = inference_co2(input_data)  # Now, input_data won't contain vehicle_id

        # Update the vehicle with predicted CO₂ emission
        update_success = VehicleService.update_vehicle(vehicle_id, {'CO2_Emission': prediction})

        if not update_success:
            return jsonify({'error': 'Failed to update vehicle data'}), 500

        return jsonify({
            'predicted_co2_emission': prediction,
            'message': 'Vehicle CO2 emission updated successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
