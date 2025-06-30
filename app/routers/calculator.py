from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import logging

from app.models.schemas import TBMParameters, AdvanceRateResult, SoilType, TBMType
from app.services.calculator import TBMAdvanceRateCalculator

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize calculator service
calculator_service = TBMAdvanceRateCalculator()

@router.post("/calculate", response_model=AdvanceRateResult)
async def calculate_advance_rate(parameters: TBMParameters):
    """
    Calculate TBM advance rate based on input parameters
    
    This endpoint uses multiple calculation methods (empirical, theoretical, and regression)
    to provide accurate advance rate predictions for tunnel boring machines.
    """
    try:
        logger.info(f"Calculating advance rate for TBM diameter: {parameters.tbm_diameter}m")
        result = calculator_service.calculate_advance_rate(parameters)
        logger.info(f"Calculation completed: {result.advance_rate} mm/min")
        return result
    except Exception as e:
        logger.error(f"Error calculating advance rate: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@router.get("/examples", response_model=List[Dict[str, Any]])
async def get_example_scenarios():
    """
    Get example TBM scenarios for different tunnel types
    
    Returns pre-configured examples for:
    - Metro/subway tunnels
    - Highway tunnels
    - Water tunnels
    - Mining tunnels
    """
    examples = [
        {
            "name": "Metro Tunnel - Soft Ground",
            "description": "Typical metro tunnel in urban soft ground conditions",
            "parameters": {
                "tbm_diameter": 6.2,
                "tbm_type": TBMType.EPB,
                "cutterhead_power": 2000,
                "soil_type": SoilType.CLAY,
                "thrust_force": 15000,
                "cutterhead_speed": 2.5,
                "depth": 15,
                "water_pressure": 1.5,
                "chamber_pressure": 1.2,
                "temperature": 18
            }
        },
        {
            "name": "Highway Tunnel - Mixed Ground",
            "description": "Highway tunnel through mixed soil and rock conditions",
            "parameters": {
                "tbm_diameter": 12.5,
                "tbm_type": TBMType.MIXSHIELD,
                "cutterhead_power": 5000,
                "soil_type": SoilType.MIXED,
                "thrust_force": 35000,
                "cutterhead_speed": 1.8,
                "depth": 40,
                "water_pressure": 3.5,
                "chamber_pressure": 2.8,
                "temperature": 22
            }
        },
        {
            "name": "Water Tunnel - Hard Rock",
            "description": "Water supply tunnel in hard rock conditions",
            "parameters": {
                "tbm_diameter": 4.5,
                "tbm_type": TBMType.OPEN,
                "cutterhead_power": 1500,
                "soil_type": SoilType.ROCK_HARD,
                "ucs": 150,
                "rqd": 85,
                "thrust_force": 8000,
                "cutterhead_speed": 3.5,
                "depth": 80,
                "water_pressure": 6.0,
                "chamber_pressure": 0,
                "temperature": 25
            }
        },
        {
            "name": "Mining Tunnel - Soft Rock",
            "description": "Mining access tunnel in soft rock",
            "parameters": {
                "tbm_diameter": 3.5,
                "tbm_type": TBMType.OPEN,
                "cutterhead_power": 800,
                "soil_type": SoilType.ROCK_SOFT,
                "ucs": 45,
                "rqd": 65,
                "thrust_force": 5000,
                "cutterhead_speed": 4.0,
                "depth": 120,
                "water_pressure": 2.0,
                "chamber_pressure": 0,
                "temperature": 30
            }
        },
        {
            "name": "Slurry TBM - Sandy Ground",
            "description": "Large diameter tunnel using slurry TBM in sandy conditions",
            "parameters": {
                "tbm_diameter": 15.2,
                "tbm_type": TBMType.SLURRY,
                "cutterhead_power": 7500,
                "soil_type": SoilType.SAND,
                "thrust_force": 45000,
                "cutterhead_speed": 1.2,
                "depth": 25,
                "water_pressure": 2.5,
                "chamber_pressure": 2.0,
                "temperature": 20
            }
        }
    ]
    
    logger.info("Returning example scenarios")
    return examples

@router.get("/soil-types")
async def get_soil_types():
    """Get available soil/rock types for TBM calculations"""
    return {
        "soil_types": [
            {"value": SoilType.CLAY, "label": "Clay", "description": "Cohesive fine-grained soil"},
            {"value": SoilType.SAND, "label": "Sand", "description": "Granular soil with good drainage"},
            {"value": SoilType.SILT, "label": "Silt", "description": "Fine-grained soil with low plasticity"},
            {"value": SoilType.GRAVEL, "label": "Gravel", "description": "Coarse granular material"},
            {"value": SoilType.ROCK_SOFT, "label": "Soft Rock", "description": "Weathered or weak rock (UCS < 50 MPa)"},
            {"value": SoilType.ROCK_MEDIUM, "label": "Medium Rock", "description": "Medium strength rock (UCS 50-100 MPa)"},
            {"value": SoilType.ROCK_HARD, "label": "Hard Rock", "description": "Strong rock (UCS > 100 MPa)"},
            {"value": SoilType.MIXED, "label": "Mixed", "description": "Variable ground conditions"},
        ]
    }

@router.get("/tbm-types")
async def get_tbm_types():
    """Get available TBM types for calculations"""
    return {
        "tbm_types": [
            {"value": TBMType.EPB, "label": "EPB (Earth Pressure Balance)", "description": "Suitable for cohesive soils and mixed ground"},
            {"value": TBMType.SLURRY, "label": "Slurry TBM", "description": "Ideal for granular soils and high water pressure"},
            {"value": TBMType.OPEN, "label": "Open TBM", "description": "Used for stable rock conditions"},
            {"value": TBMType.MIXSHIELD, "label": "Mix Shield", "description": "Versatile for changing ground conditions"},
        ]
    }

@router.get("/calculation-info")
async def get_calculation_info():
    """Get information about calculation methods and parameters"""
    return {
        "methods": {
            "empirical": {
                "name": "Empirical Method",
                "description": "Based on field data correlations and industry best practices",
                "weight": 0.4,
                "suitable_for": ["All soil types", "Established ground conditions"]
            },
            "theoretical": {
                "name": "Theoretical Method", 
                "description": "Rock/soil mechanics principles with UCS calculations",
                "weight": 0.35,
                "suitable_for": ["Rock conditions", "When UCS/RQD data available"]
            },
            "regression": {
                "name": "Regression Method",
                "description": "Machine learning-based predictions with feature engineering",
                "weight": 0.25,
                "suitable_for": ["Complex conditions", "Large datasets"]
            }
        },
        "parameters": {
            "required": [
                "tbm_diameter", "tbm_type", "cutterhead_power", 
                "soil_type", "thrust_force", "cutterhead_speed", "depth"
            ],
            "optional_for_rock": ["ucs", "rqd"],
            "optional": ["water_pressure", "chamber_pressure", "temperature"]
        },
        "output_metrics": [
            "advance_rate (mm/min)",
            "daily_advance (m/day)", 
            "penetration_rate (mm/rev)",
            "specific_energy (kWh/m³)",
            "confidence_score (0-1)",
            "risk_factors"
        ]
    }
