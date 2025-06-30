import pytest
from pydantic import ValidationError
from app.models.schemas import TBMParameters, SoilType, TBMType

def test_valid_parameters():
    """Test validation with valid parameters"""
    valid_params = {
        "tbm_diameter": 6.2,
        "tbm_type": "epb",
        "cutterhead_power": 2500,
        "soil_type": "mixed",
        "thrust_force": 35000,
        "cutterhead_speed": 2.5,
        "depth": 25
    }
    
    params = TBMParameters(**valid_params)
    assert params.tbm_diameter == 6.2
    assert params.tbm_type == TBMType.EPB
    assert params.soil_type == SoilType.MIXED

def test_diameter_validation():
    """Test TBM diameter validation"""
    base_params = {
        "tbm_type": "epb",
        "cutterhead_power": 2500,
        "soil_type": "mixed",
        "thrust_force": 35000,
        "cutterhead_speed": 2.5,
        "depth": 25
    }
    
    # Valid diameter
    params = TBMParameters(tbm_diameter=6.2, **base_params)
    assert params.tbm_diameter == 6.2
    
    # Too small
    with pytest.raises(ValidationError):
        TBMParameters(tbm_diameter=0.5, **base_params)
    
    # Too large
    with pytest.raises(ValidationError):
        TBMParameters(tbm_diameter=25.0, **base_params)

def test_power_validation():
    """Test cutterhead power validation"""
    base_params = {
        "tbm_diameter": 6.2,
        "tbm_type": "epb",
        "soil_type": "mixed",
        "thrust_force": 35000,
        "cutterhead_speed": 2.5,
        "depth": 25
    }
    
    # Valid power
    params = TBMParameters(cutterhead_power=2500, **base_params)
    assert params.cutterhead_power == 2500
    
    # Too small
    with pytest.raises(ValidationError):
        TBMParameters(cutterhead_power=50, **base_params)
    
    # Too large
    with pytest.raises(ValidationError):
        TBMParameters(cutterhead_power=15000, **base_params)

def test_thrust_force_validation():
    """Test thrust force validation"""
    base_params = {
        "tbm_diameter": 6.2,
        "tbm_type": "epb",
        "cutterhead_power": 2500,
        "soil_type": "mixed",
        "cutterhead_speed": 2.5,
        "depth": 25
    }
    
    # Valid thrust force
    params = TBMParameters(thrust_force=35000, **base_params)
    assert params.thrust_force == 35000
    
    # Too small
    with pytest.raises(ValidationError):
        TBMParameters(thrust_force=50, **base_params)
    
    # Too large
    with pytest.raises(ValidationError):
        TBMParameters(thrust_force=60000, **base_params)

def test_cutterhead_speed_validation():
    """Test cutterhead speed validation"""
    base_params = {
        "tbm_diameter": 6.2,
        "tbm_type": "epb",
        "cutterhead_power": 2500,
        "soil_type": "mixed",
        "thrust_force": 35000,
        "depth": 25
    }
    
    # Valid speed
    params = TBMParameters(cutterhead_speed=2.5, **base_params)
    assert params.cutterhead_speed == 2.5
    
    # Too small
    with pytest.raises(ValidationError):
        TBMParameters(cutterhead_speed=0.05, **base_params)
    
    # Too large
    with pytest.raises(ValidationError):
        TBMParameters(cutterhead_speed=15.0, **base_params)

def test_depth_validation():
    """Test depth validation"""
    base_params = {
        "tbm_diameter": 6.2,
        "tbm_type": "epb",
        "cutterhead_power": 2500,
        "soil_type": "mixed",
        "thrust_force": 35000,
        "cutterhead_speed": 2.5
    }
    
    # Valid depth
    params = TBMParameters(depth=25, **base_params)
    assert params.depth == 25
    
    # Too small
    with pytest.raises(ValidationError):
        TBMParameters(depth=0, **base_params)
    
    # Too large
    with pytest.raises(ValidationError):
        TBMParameters(depth=250, **base_params)

def test_ucs_validation_for_rock():
    """Test UCS validation for rock types"""
    base_params = {
        "tbm_diameter": 8.5,
        "tbm_type": "open",
        "cutterhead_power": 4500,
        "thrust_force": 60000,
        "cutterhead_speed": 1.2,
        "depth": 80
    }
    
    # Rock type without UCS should fail
    with pytest.raises(ValidationError):
        TBMParameters(soil_type="rock_hard", **base_params)
    
    # Rock type with UCS should pass
    params = TBMParameters(
        soil_type="rock_hard",
        ucs=120,
        rqd=85,
        **base_params
    )
    assert params.ucs == 120
    assert params.rqd == 85

def test_rqd_validation_for_rock():
    """Test RQD validation for rock types"""
    base_params = {
        "tbm_diameter": 8.5,
        "tbm_type": "open",
        "cutterhead_power": 4500,
        "thrust_force": 60000,
        "cutterhead_speed": 1.2,
        "depth": 80,
        "ucs": 120
    }
    
    # Rock type without RQD should fail
    with pytest.raises(ValidationError):
        TBMParameters(soil_type="rock_medium", **base_params)
    
    # Valid RQD range
    params = TBMParameters(
        soil_type="rock_medium",
        rqd=75,
        **base_params
    )
    assert params.rqd == 75
    
    # Invalid RQD (too high)
    with pytest.raises(ValidationError):
        TBMParameters(
            soil_type="rock_medium",
            rqd=150,
            **base_params
        )

def test_soil_type_no_ucs_required():
    """Test that soil types don't require UCS"""
    params = TBMParameters(
        tbm_diameter=6.2,
        tbm_type="epb",
        cutterhead_power=2500,
        soil_type="clay",  # Soil type, no UCS required
        thrust_force=35000,
        cutterhead_speed=2.5,
        depth=25
    )
    
    assert params.soil_type == SoilType.CLAY
    assert params.ucs is None
    assert params.rqd is None

def test_optional_parameters():
    """Test optional parameters with default values"""
    params = TBMParameters(
        tbm_diameter=6.2,
        tbm_type="epb",
        cutterhead_power=2500,
        soil_type="mixed",
        thrust_force=35000,
        cutterhead_speed=2.5,
        depth=25
    )
    
    # Check default values
    assert params.water_pressure == 0
    assert params.chamber_pressure == 0
    assert params.temperature == 20
    assert params.ucs is None
    assert params.rqd is None

def test_pressure_validation():
    """Test pressure parameter validation"""
    base_params = {
        "tbm_diameter": 6.2,
        "tbm_type": "epb",
        "cutterhead_power": 2500,
        "soil_type": "mixed",
        "thrust_force": 35000,
        "cutterhead_speed": 2.5,
        "depth": 25
    }
    
    # Valid pressures
    params = TBMParameters(
        water_pressure=3.5,
        chamber_pressure=2.0,
        **base_params
    )
    assert params.water_pressure == 3.5
    assert params.chamber_pressure == 2.0
    
    # Invalid water pressure (too high)
    with pytest.raises(ValidationError):
        TBMParameters(water_pressure=15.0, **base_params)
    
    # Invalid chamber pressure (negative)
    with pytest.raises(ValidationError):
        TBMParameters(chamber_pressure=-1.0, **base_params)

def test_temperature_validation():
    """Test temperature validation"""
    base_params = {
        "tbm_diameter": 6.2,
        "tbm_type": "epb",
        "cutterhead_power": 2500,
        "soil_type": "mixed",
        "thrust_force": 35000,
        "cutterhead_speed": 2.5,
        "depth": 25
    }
    
    # Valid temperature
    params = TBMParameters(temperature=15, **base_params)
    assert params.temperature == 15
    
    # Too cold
    with pytest.raises(ValidationError):
        TBMParameters(temperature=-20, **base_params)
    
    # Too hot
    with pytest.raises(ValidationError):
        TBMParameters(temperature=80, **base_params)

def test_tbm_type_enum():
    """Test TBM type enumeration"""
    base_params = {
        "tbm_diameter": 6.2,
        "cutterhead_power": 2500,
        "soil_type": "mixed",
        "thrust_force": 35000,
        "cutterhead_speed": 2.5,
        "depth": 25
    }
    
    # Valid TBM types
    for tbm_type in ["epb", "slurry", "open", "mixshield"]:
        params = TBMParameters(tbm_type=tbm_type, **base_params)
        assert params.tbm_type.value == tbm_type
    
    # Invalid TBM type
    with pytest.raises(ValidationError):
        TBMParameters(tbm_type="invalid_type", **base_params)

def test_soil_type_enum():
    """Test soil type enumeration"""
    base_params = {
        "tbm_diameter": 6.2,
        "tbm_type": "epb",
        "cutterhead_power": 2500,
        "thrust_force": 35000,
        "cutterhead_speed": 2.5,
        "depth": 25
    }
    
    # Valid soil types
    soil_types = ["clay", "sand", "silt", "gravel", "mixed"]
    for soil_type in soil_types:
        params = TBMParameters(soil_type=soil_type, **base_params)
        assert params.soil_type.value == soil_type
    
    # Invalid soil type
    with pytest.raises(ValidationError):
        TBMParameters(soil_type="invalid_soil", **base_params)