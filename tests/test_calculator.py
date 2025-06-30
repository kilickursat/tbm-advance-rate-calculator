import pytest
import math
from app.services.calculator import TBMAdvanceRateCalculator
from app.models.schemas import TBMParameters, SoilType, TBMType

def test_calculator_initialization(calculator: TBMAdvanceRateCalculator):
    """Test calculator initialization"""
    assert calculator is not None
    assert len(calculator.soil_coefficients) > 0
    assert len(calculator.tbm_efficiency) > 0

def test_empirical_method(calculator: TBMAdvanceRateCalculator, sample_parameters):
    """Test empirical calculation method"""
    params = TBMParameters(**sample_parameters)
    result = calculator._empirical_method(params)
    
    assert result > 0
    assert result < 100  # Reasonable upper bound

def test_theoretical_method_soil(calculator: TBMAdvanceRateCalculator, sample_parameters):
    """Test theoretical method for soil conditions"""
    params = TBMParameters(**sample_parameters)
    result = calculator._theoretical_method(params)
    
    assert result > 0
    assert result < 100

def test_theoretical_method_rock(calculator: TBMAdvanceRateCalculator, rock_parameters):
    """Test theoretical method for rock conditions"""
    params = TBMParameters(**rock_parameters)
    result = calculator._theoretical_method(params)
    
    assert result > 0
    assert result < 50  # Rock typically has lower advance rates

def test_regression_method(calculator: TBMAdvanceRateCalculator, sample_parameters):
    """Test regression calculation method"""
    params = TBMParameters(**sample_parameters)
    result = calculator._regression_method(params)
    
    assert result > 0
    assert result < 100

def test_calculate_advance_rate(calculator: TBMAdvanceRateCalculator, sample_parameters):
    """Test main calculation method"""
    params = TBMParameters(**sample_parameters)
    result = calculator.calculate_advance_rate(params)
    
    # Check result structure
    assert result.advance_rate > 0
    assert result.daily_advance > 0
    assert result.penetration_rate >= 0
    assert result.specific_energy >= 0
    assert 0 <= result.confidence_score <= 1
    assert result.risk_factors is not None
    assert result.calculation_method is not None
    
    # Check risk factors structure
    assert "risks" in result.risk_factors
    assert "recommendations" in result.risk_factors
    assert "overall_risk_level" in result.risk_factors

def test_calculate_advance_rate_rock(calculator: TBMAdvanceRateCalculator, rock_parameters):
    """Test calculation with rock parameters"""
    params = TBMParameters(**rock_parameters)
    result = calculator.calculate_advance_rate(params)
    
    assert result.advance_rate > 0
    # Rock conditions typically have lower advance rates
    assert result.advance_rate < 20

def test_penetration_rate_calculation(calculator: TBMAdvanceRateCalculator):
    """Test penetration rate calculation"""
    advance_rate = 10.0  # mm/min
    rpm = 2.0
    
    penetration_rate = calculator._calculate_penetration_rate(advance_rate, rpm)
    expected = advance_rate / rpm
    
    assert penetration_rate == expected
    
    # Test with zero RPM
    zero_rpm_result = calculator._calculate_penetration_rate(advance_rate, 0)
    assert zero_rpm_result == 0

def test_specific_energy_calculation(calculator: TBMAdvanceRateCalculator, sample_parameters):
    """Test specific energy calculation"""
    params = TBMParameters(**sample_parameters)
    advance_rate = 10.0  # mm/min
    
    specific_energy = calculator._calculate_specific_energy(params, advance_rate)
    assert specific_energy >= 0

def test_daily_advance_calculation(calculator: TBMAdvanceRateCalculator):
    """Test daily advance calculation"""
    advance_rate = 10.0  # mm/min
    
    daily_advance = calculator._calculate_daily_advance(advance_rate)
    expected = advance_rate * 60 * 20 / 1000  # 20 hours operation
    
    assert daily_advance == expected

def test_confidence_score_calculation(calculator: TBMAdvanceRateCalculator, sample_parameters):
    """Test confidence score calculation"""
    params = TBMParameters(**sample_parameters)
    rates = {"empirical": 10.0, "theoretical": 12.0, "regression": 11.0}
    
    confidence = calculator._calculate_confidence_score(params, rates)
    
    assert 0 <= confidence <= 1

def test_risk_assessment(calculator: TBMAdvanceRateCalculator):
    """Test risk assessment functionality"""
    # High water pressure scenario
    high_water_params = TBMParameters(
        tbm_diameter=6.0,
        tbm_type=TBMType.EPB,
        cutterhead_power=2000,
        soil_type=SoilType.CLAY,
        thrust_force=30000,
        cutterhead_speed=2.0,
        depth=20,
        water_pressure=5.0  # High water pressure
    )
    
    risk_factors = calculator._assess_risk_factors(high_water_params)
    
    assert "risks" in risk_factors
    assert "recommendations" in risk_factors
    assert "overall_risk_level" in risk_factors
    
    # Should identify high water pressure risk
    if "high_water_pressure" in risk_factors["risks"]:
        assert risk_factors["risks"]["high_water_pressure"]["level"] == "high"

def test_method_weights(calculator: TBMAdvanceRateCalculator, sample_parameters):
    """Test method weight calculation"""
    params = TBMParameters(**sample_parameters)
    weights = calculator._get_method_weights(params)
    
    assert "empirical" in weights
    assert "theoretical" in weights
    assert "regression" in weights
    
    # Weights should sum to approximately 1
    total_weight = sum(weights.values())
    assert abs(total_weight - 1.0) < 0.01
    
    # All weights should be positive
    for weight in weights.values():
        assert weight > 0

def test_soil_type_coefficients(calculator: TBMAdvanceRateCalculator):
    """Test that all soil types have coefficients"""
    for soil_type in SoilType:
        assert soil_type in calculator.soil_coefficients
        coeffs = calculator.soil_coefficients[soil_type]
        assert "k1" in coeffs
        assert "k2" in coeffs
        assert "resistance" in coeffs
        assert coeffs["k1"] > 0
        assert coeffs["k2"] > 0
        assert coeffs["resistance"] > 0

def test_tbm_efficiency_factors(calculator: TBMAdvanceRateCalculator):
    """Test that all TBM types have efficiency factors"""
    for tbm_type in TBMType:
        assert tbm_type in calculator.tbm_efficiency
        efficiency = calculator.tbm_efficiency[tbm_type]
        assert 0 < efficiency <= 1

def test_extreme_parameters(calculator: TBMAdvanceRateCalculator):
    """Test calculation with extreme but valid parameters"""
    # Very large TBM
    large_tbm_params = TBMParameters(
        tbm_diameter=15.0,
        tbm_type=TBMType.EPB,
        cutterhead_power=8000,
        soil_type=SoilType.SAND,
        thrust_force=40000,
        cutterhead_speed=1.0,
        depth=100
    )
    
    result = calculator.calculate_advance_rate(large_tbm_params)
    assert result.advance_rate > 0
    
    # Very small TBM
    small_tbm_params = TBMParameters(
        tbm_diameter=2.0,
        tbm_type=TBMType.OPEN,
        cutterhead_power=500,
        soil_type=SoilType.GRAVEL,
        thrust_force=5000,
        cutterhead_speed=5.0,
        depth=10
    )
    
    result = calculator.calculate_advance_rate(small_tbm_params)
    assert result.advance_rate > 0

def test_risk_level_calculation(calculator: TBMAdvanceRateCalculator):
    """Test overall risk level calculation"""
    # No risks
    no_risks = {}
    level = calculator._calculate_overall_risk_level(no_risks)
    assert level == "low"
    
    # Medium risk
    medium_risks = {
        "risk1": {"level": "medium"}
    }
    level = calculator._calculate_overall_risk_level(medium_risks)
    assert level == "medium"
    
    # High risk
    high_risks = {
        "risk1": {"level": "medium"},
        "risk2": {"level": "high"}
    }
    level = calculator._calculate_overall_risk_level(high_risks)
    assert level == "high"