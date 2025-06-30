import math
import logging
from typing import Dict, Any
from app.models.schemas import TBMParameters, AdvanceRateResult, SoilType, TBMType

logger = logging.getLogger(__name__)

class TBMAdvanceRateCalculator:
    """Advanced TBM advance rate calculator using multiple engineering models"""
    
    def __init__(self):
        # Soil/rock coefficients for different calculation methods
        self.soil_coefficients = {
            SoilType.CLAY: {"k1": 0.8, "k2": 1.2, "resistance": 0.6},
            SoilType.SAND: {"k1": 1.0, "k2": 1.0, "resistance": 0.4},
            SoilType.SILT: {"k1": 0.9, "k2": 1.1, "resistance": 0.5},
            SoilType.GRAVEL: {"k1": 1.2, "k2": 0.9, "resistance": 0.7},
            SoilType.ROCK_SOFT: {"k1": 0.6, "k2": 1.5, "resistance": 1.2},
            SoilType.ROCK_MEDIUM: {"k1": 0.4, "k2": 2.0, "resistance": 2.0},
            SoilType.ROCK_HARD: {"k1": 0.2, "k2": 3.0, "resistance": 3.5},
            SoilType.MIXED: {"k1": 0.7, "k2": 1.3, "resistance": 1.0}
        }
        
        # TBM type efficiency factors
        self.tbm_efficiency = {
            TBMType.EPB: 0.85,
            TBMType.SLURRY: 0.80,
            TBMType.OPEN: 0.90,
            TBMType.MIXSHIELD: 0.82
        }
    
    def calculate_advance_rate(self, params: TBMParameters) -> AdvanceRateResult:
        """Calculate TBM advance rate using multiple methods"""
        
        logger.info(f"Calculating advance rate for TBM diameter: {params.tbm_diameter}m")
        
        # Use hybrid approach combining multiple methods
        rates = {
            "empirical": self._empirical_method(params),
            "theoretical": self._theoretical_method(params),
            "regression": self._regression_method(params)
        }
        
        # Weight the methods based on soil type and data availability
        weights = self._get_method_weights(params)
        
        # Calculate weighted average
        advance_rate = sum(rates[method] * weights[method] for method in rates)
        
        # Calculate derived metrics
        penetration_rate = self._calculate_penetration_rate(advance_rate, params.cutterhead_speed)
        specific_energy = self._calculate_specific_energy(params, advance_rate)
        daily_advance = self._calculate_daily_advance(advance_rate)
        confidence_score = self._calculate_confidence_score(params, rates)
        risk_factors = self._assess_risk_factors(params)
        
        result = AdvanceRateResult(
            advance_rate=round(advance_rate, 2),
            daily_advance=round(daily_advance, 2),
            penetration_rate=round(penetration_rate, 2),
            specific_energy=round(specific_energy, 2),
            confidence_score=round(confidence_score, 3),
            risk_factors=risk_factors,
            calculation_method="Hybrid (Empirical + Theoretical + Regression)"
        )
        
        logger.info(f"Calculated advance rate: {result.advance_rate} mm/min")
        return result
    
    def _empirical_method(self, params: TBMParameters) -> float:
        """Empirical method based on field data correlations"""
        
        soil_coeff = self.soil_coefficients[params.soil_type]
        tbm_eff = self.tbm_efficiency[params.tbm_type]
        
        # Base advance rate from thrust and diameter relationship
        base_rate = (params.thrust_force / (math.pi * (params.tbm_diameter/2)**2)) * 0.1
        
        # Apply soil and TBM type corrections
        advance_rate = base_rate * soil_coeff["k1"] * tbm_eff
        
        # Apply depth correction
        depth_factor = max(0.5, 1 - (params.depth - 10) * 0.01)
        advance_rate *= depth_factor
        
        # Apply water pressure correction
        water_factor = max(0.3, 1 - params.water_pressure * 0.05)
        advance_rate *= water_factor
        
        return max(0.5, advance_rate)  # Minimum advance rate
    
    def _theoretical_method(self, params: TBMParameters) -> float:
        """Theoretical method based on rock mechanics principles"""
        
        soil_coeff = self.soil_coefficients[params.soil_type]
        
        # For rock types, use UCS-based calculation
        if 'rock' in params.soil_type:
            if params.ucs:
                # Rock cutting force calculation
                cutting_force = params.cutterhead_power * 1000 / params.cutterhead_speed  # N*m/rev
                specific_cutting_force = params.ucs * 1e6 * 0.1  # N/m (simplified)
                
                # Advance rate based on cutting mechanics
                advance_rate = cutting_force / (specific_cutting_force * params.tbm_diameter * math.pi)
                advance_rate = advance_rate * params.cutterhead_speed * 60 / 1000  # mm/min
            else:
                advance_rate = 5.0  # Default for rock without UCS
        else:
            # For soil, use penetration resistance approach
            penetration_resistance = soil_coeff["resistance"] * 1000  # N/m²
            
            # Calculate advance rate from thrust and resistance
            net_thrust = params.thrust_force * 1000 - params.chamber_pressure * 1e5 * math.pi * (params.tbm_diameter/2)**2
            advance_rate = net_thrust / (penetration_resistance * math.pi * params.tbm_diameter)
            advance_rate = min(advance_rate * 60 / 1000, 50.0)  # mm/min, capped at 50
        
        # Apply operational efficiency
        efficiency = min(1.0, params.cutterhead_power / (params.tbm_diameter**2 * 200))  # Power adequacy
        advance_rate *= efficiency
        
        return max(0.5, advance_rate)
    
    def _regression_method(self, params: TBMParameters) -> float:
        """Machine learning-based regression method (simplified model)"""
        
        # Simplified regression model based on common TBM parameters
        # In production, this would be replaced with a trained ML model
        
        # Feature engineering
        features = {
            'diameter': params.tbm_diameter,
            'power_per_area': params.cutterhead_power / (math.pi * (params.tbm_diameter/2)**2),
            'thrust_per_area': params.thrust_force / (math.pi * (params.tbm_diameter/2)**2),
            'rotation_speed': params.cutterhead_speed,
            'depth_factor': 1 / (1 + params.depth * 0.01),
            'soil_hardness': self.soil_coefficients[params.soil_type]['resistance']
        }
        
        # Simplified linear regression coefficients (would be learned from data)
        coefficients = {
            'intercept': 2.5,
            'diameter': -0.8,
            'power_per_area': 0.15,
            'thrust_per_area': 0.008,
            'rotation_speed': 1.2,
            'depth_factor': 3.0,
            'soil_hardness': -2.1
        }
        
        # Calculate prediction
        advance_rate = coefficients['intercept']
        for feature, value in features.items():
            if feature in coefficients:
                advance_rate += coefficients[feature] * value
        
        # Apply bounds
        advance_rate = max(0.5, min(advance_rate, 45.0))
        
        return advance_rate
    
    def _get_method_weights(self, params: TBMParameters) -> Dict[str, float]:
        """Determine weights for different calculation methods"""
        
        # Default weights
        weights = {"empirical": 0.4, "theoretical": 0.35, "regression": 0.25}
        
        # Adjust based on data availability and soil type
        if 'rock' in params.soil_type and params.ucs and params.rqd:
            weights["theoretical"] += 0.1
            weights["empirical"] -= 0.05
            weights["regression"] -= 0.05
        
        # For very large or small TBMs, favor empirical data
        if params.tbm_diameter > 12 or params.tbm_diameter < 3:
            weights["empirical"] += 0.1
            weights["theoretical"] -= 0.05
            weights["regression"] -= 0.05
        
        return weights
    
    def _calculate_penetration_rate(self, advance_rate: float, rpm: float) -> float:
        """Calculate penetration rate in mm per revolution"""
        if rpm > 0:
            return advance_rate / rpm
        return 0
    
    def _calculate_specific_energy(self, params: TBMParameters, advance_rate: float) -> float:
        """Calculate specific energy in kWh/m³"""
        if advance_rate > 0:
            # Volume excavated per minute
            volume_rate = math.pi * (params.tbm_diameter/2)**2 * (advance_rate/1000) / 60  # m³/s
            if volume_rate > 0:
                return params.cutterhead_power / (volume_rate * 3600)  # kWh/m³
        return 0
    
    def _calculate_daily_advance(self, advance_rate: float) -> float:
        """Calculate daily advance assuming 20 hours of operation"""
        return advance_rate * 60 * 20 / 1000  # meters per day
    
    def _calculate_confidence_score(self, params: TBMParameters, rates: Dict[str, float]) -> float:
        """Calculate confidence score based on parameter completeness and rate consistency"""
        
        # Base confidence from parameter completeness
        required_params = 8  # Basic required parameters
        available_params = required_params
        
        if params.ucs is not None:
            available_params += 1
        if params.rqd is not None:
            available_params += 1
        
        completeness_score = min(1.0, available_params / 10)
        
        # Consistency score from rate variations
        rate_values = list(rates.values())
        mean_rate = sum(rate_values) / len(rate_values)
        variance = sum((rate - mean_rate)**2 for rate in rate_values) / len(rate_values)
        consistency_score = max(0.3, 1 - math.sqrt(variance) / mean_rate)
        
        # Operational feasibility score
        feasibility_score = 1.0
        if params.thrust_force / (math.pi * (params.tbm_diameter/2)**2) > 5000:  # kN/m²
            feasibility_score *= 0.9
        if params.cutterhead_power / (math.pi * (params.tbm_diameter/2)**2) < 100:  # kW/m²
            feasibility_score *= 0.8
        
        return (completeness_score * 0.4 + consistency_score * 0.4 + feasibility_score * 0.2)
    
    def _assess_risk_factors(self, params: TBMParameters) -> Dict[str, Any]:
        """Assess operational risks and provide recommendations"""
        
        risks = {}
        recommendations = []
        
        # Check for high water pressure
        if params.water_pressure > 3:
            risks["high_water_pressure"] = {
                "level": "high",
                "description": f"Water pressure of {params.water_pressure} bar may cause stability issues"
            }
            recommendations.append("Consider additional ground treatment or pressure relief measures")
        
        # Check for inadequate power
        power_per_area = params.cutterhead_power / (math.pi * (params.tbm_diameter/2)**2)
        if power_per_area < 150:
            risks["low_power"] = {
                "level": "medium",
                "description": f"Power density of {power_per_area:.1f} kW/m² may be insufficient"
            }
            recommendations.append("Monitor power consumption and consider reducing advance rate if needed")
        
        # Check for extreme depth
        if params.depth > 50:
            risks["deep_tunneling"] = {
                "level": "medium",
                "description": f"Depth of {params.depth}m requires careful pressure management"
            }
            recommendations.append("Implement enhanced monitoring and ground settlement controls")
        
        # Check for hard rock conditions
        if 'rock' in params.soil_type and params.ucs and params.ucs > 100:
            risks["hard_rock"] = {
                "level": "high",
                "description": f"UCS of {params.ucs} MPa indicates very hard rock conditions"
            }
            recommendations.append("Plan for increased cutter wear and potential advance rate reductions")
        
        return {
            "risks": risks,
            "recommendations": recommendations,
            "overall_risk_level": self._calculate_overall_risk_level(risks)
        }
    
    def _calculate_overall_risk_level(self, risks: Dict[str, Any]) -> str:
        """Calculate overall risk level"""
        if not risks:
            return "low"
        
        risk_levels = [risk["level"] for risk in risks.values()]
        
        if "high" in risk_levels:
            return "high"
        elif "medium" in risk_levels:
            return "medium"
        else:
            return "low"