from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from enum import Enum

class SoilType(str, Enum):
    CLAY = "clay"
    SAND = "sand"
    SILT = "silt"
    GRAVEL = "gravel"
    ROCK_SOFT = "rock_soft"
    ROCK_MEDIUM = "rock_medium"
    ROCK_HARD = "rock_hard"
    MIXED = "mixed"

class TBMType(str, Enum):
    EPB = "epb"  # Earth Pressure Balance
    SLURRY = "slurry"  # Slurry TBM
    OPEN = "open"  # Open TBM
    MIXSHIELD = "mixshield"  # Mix Shield

class TBMParameters(BaseModel):
    """Input parameters for TBM advance rate calculation"""
    
    # TBM Specifications
    tbm_diameter: float = Field(
        ..., 
        ge=1.0, 
        le=20.0, 
        description="TBM diameter in meters"
    )
    tbm_type: TBMType = Field(
        ..., 
        description="Type of TBM"
    )
    cutterhead_power: float = Field(
        ..., 
        ge=100, 
        le=10000, 
        description="Cutterhead power in kW"
    )
    
    # Geological Parameters
    soil_type: SoilType = Field(
        ..., 
        description="Primary soil/rock type"
    )
    ucs: Optional[float] = Field(
        None, 
        ge=0, 
        le=300, 
        description="Unconfined compressive strength in MPa"
    )
    rqd: Optional[float] = Field(
        None, 
        ge=0, 
        le=100, 
        description="Rock Quality Designation (%)"
    )
    water_pressure: float = Field(
        0, 
        ge=0, 
        le=10, 
        description="Water pressure in bar"
    )
    
    # Operational Parameters
    thrust_force: float = Field(
        ..., 
        ge=100, 
        le=50000, 
        description="Thrust force in kN"
    )
    cutterhead_speed: float = Field(
        ..., 
        ge=0.1, 
        le=10.0, 
        description="Cutterhead rotation speed in RPM"
    )
    chamber_pressure: float = Field(
        0, 
        ge=0, 
        le=10, 
        description="Chamber pressure in bar"
    )
    
    # Environmental Conditions
    depth: float = Field(
        ..., 
        ge=1, 
        le=200, 
        description="Depth below surface in meters"
    )
    temperature: float = Field(
        20, 
        ge=-10, 
        le=60, 
        description="Ground temperature in Celsius"
    )
    
    @field_validator('ucs')
    @classmethod
    def validate_ucs_for_rock(cls, v, info):
        # Access other field values through info.data
        if hasattr(info, 'data') and info.data:
            soil_type = info.data.get('soil_type')
            if soil_type and 'rock' in soil_type and v is None:
                raise ValueError('UCS is required for rock types')
        return v
    
    @field_validator('rqd')
    @classmethod
    def validate_rqd_for_rock(cls, v, info):
        # Access other field values through info.data
        if hasattr(info, 'data') and info.data:
            soil_type = info.data.get('soil_type')
            if soil_type and 'rock' in soil_type and v is None:
                raise ValueError('RQD is required for rock types')
        return v

class AdvanceRateResult(BaseModel):
    """Result of advance rate calculation"""
    
    advance_rate: float = Field(
        ..., 
        description="Predicted advance rate in mm/min"
    )
    daily_advance: float = Field(
        ..., 
        description="Daily advance in meters (assuming 20h operation)"
    )
    penetration_rate: float = Field(
        ..., 
        description="Penetration rate in mm/rev"
    )
    specific_energy: float = Field(
        ..., 
        description="Specific energy in kWh/m³"
    )
    confidence_score: float = Field(
        ..., 
        ge=0, 
        le=1, 
        description="Confidence score of the prediction (0-1)"
    )
    risk_factors: Dict[str, Any] = Field(
        ..., 
        description="Identified risk factors and recommendations"
    )
    calculation_method: str = Field(
        ..., 
        description="Method used for calculation"
    )

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    uptime: float
