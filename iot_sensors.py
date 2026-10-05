"""
IoT Sensor Simulation Module for Smart Parking System

This module simulates IoT-based sensors (ultrasonic and infrared) used for vehicle detection
in parking slots. It includes sensor data generation, anomaly detection, and alert generation.

Author: Internship Project Team
Date: 2024
"""

import random
import datetime
import json
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SensorType(Enum):
    """Types of sensors used in parking system"""
    ULTRASONIC = "Ultrasonic"
    INFRARED = "Infrared"
    PRESSURE = "Pressure"
    MAGNETIC = "Magnetic"


class SensorStatus(Enum):
    """Status of sensor"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    FAULTY = "Faulty"
    MAINTENANCE = "Maintenance"


@dataclass
class SensorReading:
    """Data class for sensor reading"""
    sensor_id: str
    timestamp: datetime.datetime
    reading_value: float  # Distance in cm for ultrasonic, binary for infrared
    sensor_type: SensorType
    slot_id: str
    status: SensorStatus
    confidence: float  # 0.0 to 1.0
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'sensor_id': self.sensor_id,
            'timestamp': self.timestamp.isoformat(),
            'reading_value': self.reading_value,
            'sensor_type': self.sensor_type.value,
            'slot_id': self.slot_id,
            'status': self.status.value,
            'confidence': self.confidence
        }


@dataclass
class SensorAlert:
    """Data class for sensor alert"""
    alert_id: str
    sensor_id: str
    alert_type: str  # 'ANOMALY', 'FAILURE', 'CALIBRATION_NEEDED'
    severity: str  # 'LOW', 'MEDIUM', 'HIGH'
    message: str
    timestamp: datetime.datetime
    resolved: bool = False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'sensor_id': self.sensor_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved
        }


class IoTSensor:
    """Base class for IoT sensors"""
    
    def __init__(self, sensor_id: str, sensor_type: SensorType, slot_id: str):
        """Initialize sensor"""
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.slot_id = slot_id
        self.status = SensorStatus.ACTIVE
        self.last_reading = None
        self.readings_history: List[SensorReading] = []
        self.alerts: List[SensorAlert] = []
        self.calibration_needed = False
        self.battery_level = 100.0  # Battery percentage
    
    def take_reading(self, vehicle_present: bool = False) -> SensorReading:
        """
        Take a sensor reading
        
        Args:
            vehicle_present: Whether a vehicle is present in the slot
            
        Returns:
            SensorReading object
        """
        timestamp = datetime.datetime.now()
        
        if self.sensor_type == SensorType.ULTRASONIC:
            reading_value = self._get_ultrasonic_reading(vehicle_present)
        elif self.sensor_type == SensorType.INFRARED:
            reading_value = self._get_infrared_reading(vehicle_present)
        elif self.sensor_type == SensorType.PRESSURE:
            reading_value = self._get_pressure_reading(vehicle_present)
        elif self.sensor_type == SensorType.MAGNETIC:
            reading_value = self._get_magnetic_reading(vehicle_present)
        
        # Calculate confidence based on battery and sensor health
        confidence = self._calculate_confidence()
        
        # Create reading object
        reading = SensorReading(
            sensor_id=self.sensor_id,
            timestamp=timestamp,
            reading_value=reading_value,
            sensor_type=self.sensor_type,
            slot_id=self.slot_id,
            status=self.status,
            confidence=confidence
        )
        
        self.last_reading = reading
        self.readings_history.append(reading)
        
        # Simulate battery drain
        self.battery_level -= random.uniform(0.01, 0.05)
        
        # Check for anomalies
        self._check_anomalies(reading)
        
        return reading
    
    def _get_ultrasonic_reading(self, vehicle_present: bool) -> float:
        """Generate ultrasonic sensor reading (distance in cm)"""
        if vehicle_present:
            # Vehicle present: distance 5-15 cm
            return random.uniform(5, 15) + random.gauss(0, 0.5)
        else:
            # No vehicle: distance 180-200 cm (max range)
            return random.uniform(180, 200) + random.gauss(0, 2)
    
    def _get_infrared_reading(self, vehicle_present: bool) -> float:
        """Generate infrared sensor reading (binary: 0 or 1)"""
        if vehicle_present:
            # Vehicle present: return 1 with high probability
            return 1.0 if random.random() > 0.05 else 0.0
        else:
            # No vehicle: return 0 with high probability
            return 0.0 if random.random() > 0.05 else 1.0
    
    def _get_pressure_reading(self, vehicle_present: bool) -> float:
        """Generate pressure sensor reading (kg)"""
        if vehicle_present:
            # Vehicle weight: 1000-2000 kg
            return random.uniform(1000, 2000) + random.gauss(0, 50)
        else:
            # No vehicle: 0 kg
            return random.uniform(0, 50) + random.gauss(0, 5)
    
    def _get_magnetic_reading(self, vehicle_present: bool) -> float:
        """Generate magnetic sensor reading (magnetic field strength)"""
        if vehicle_present:
            # Vehicle present: high magnetic field
            return random.uniform(100, 150) + random.gauss(0, 10)
        else:
            # No vehicle: low magnetic field
            return random.uniform(0, 20) + random.gauss(0, 2)
    
    def _calculate_confidence(self) -> float:
        """Calculate confidence score for the reading"""
        confidence = 1.0
        
        # Reduce confidence if battery is low
        if self.battery_level < 20:
            confidence *= 0.7
        elif self.battery_level < 50:
            confidence *= 0.85
        
        # Reduce confidence if sensor needs calibration
        if self.calibration_needed:
            confidence *= 0.6
        
        # Reduce confidence if sensor is faulty
        if self.status == SensorStatus.FAULTY:
            confidence *= 0.3
        
        return max(0.0, min(1.0, confidence))
    
    def _check_anomalies(self, reading: SensorReading):
        """Check for sensor anomalies"""
        # Check for sudden spikes in readings
        if len(self.readings_history) > 1:
            prev_reading = self.readings_history[-2].reading_value
            current_reading = reading.reading_value
            
            # For ultrasonic sensor
            if self.sensor_type == SensorType.ULTRASONIC:
                if abs(current_reading - prev_reading) > 50:
                    alert = SensorAlert(
                        alert_id=f"ALERT_{len(self.alerts) + 1}",
                        sensor_id=self.sensor_id,
                        alert_type="ANOMALY",
                        severity="MEDIUM",
                        message=f"Sudden spike detected in ultrasonic reading: {prev_reading} -> {current_reading}",
                        timestamp=datetime.datetime.now()
                    )
                    self.alerts.append(alert)
                    logger.warning(f"Anomaly detected in sensor {self.sensor_id}: {alert.message}")
        
        # Check battery level
        if self.battery_level < 10:
            alert = SensorAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                alert_type="FAILURE",
                severity="HIGH",
                message=f"Battery level critical: {self.battery_level:.1f}%",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.warning(f"Battery alert for sensor {self.sensor_id}")
    
    def calibrate(self):
        """Calibrate sensor"""
        self.calibration_needed = False
        logger.info(f"Sensor {self.sensor_id} calibrated successfully")
    
    def perform_maintenance(self):
        """Perform maintenance on sensor"""
        self.status = SensorStatus.MAINTENANCE
        self.battery_level = 100.0
        self.calibration_needed = False
        logger.info(f"Maintenance completed for sensor {self.sensor_id}")
    
    def get_health_status(self) -> Dict:
        """Get sensor health status"""
        return {
            'sensor_id': self.sensor_id,
            'sensor_type': self.sensor_type.value,
            'status': self.status.value,
            'battery_level': round(self.battery_level, 2),
            'calibration_needed': self.calibration_needed,
            'last_reading': self.last_reading.to_dict() if self.last_reading else None,
            'total_readings': len(self.readings_history),
            'active_alerts': len([a for a in self.alerts if not a.resolved])
        }


class SensorNetwork:
    """Network of IoT sensors for the parking lot"""
    
    def __init__(self, parking_lot):
        """Initialize sensor network"""
        self.parking_lot = parking_lot
        self.sensors: Dict[str, IoTSensor] = {}
        self.all_readings: List[SensorReading] = []
        self.all_alerts: List[SensorAlert] = []
        
        self._initialize_sensors()
    
    def _initialize_sensors(self):
        """Initialize sensors for all parking slots"""
        sensor_types = [SensorType.ULTRASONIC, SensorType.INFRARED, SensorType.PRESSURE]
        
        for slot_id, slot in self.parking_lot.slots.items():
            # Assign sensor type based on slot
            sensor_type = sensor_types[hash(slot_id) % len(sensor_types)]
            
            sensor_id = f"SENSOR_{slot_id}"
            sensor = IoTSensor(sensor_id, sensor_type, slot_id)
            self.sensors[sensor_id] = sensor
        
        logger.info(f"Initialized {len(self.sensors)} sensors for parking lot")
    
    def read_all_sensors(self):
        """Read all sensors in the network"""
        for sensor_id, sensor in self.sensors.items():
            slot_id = sensor.slot_id
            slot = self.parking_lot.slots[slot_id]
            
            # Determine if vehicle is present
            vehicle_present = slot.status.value == "Occupied"
            
            # Take reading
            reading = sensor.take_reading(vehicle_present)
            self.all_readings.append(reading)
            
            # Collect alerts
            for alert in sensor.alerts:
                if not alert.resolved:
                    self.all_alerts.append(alert)
    
    def get_network_health(self) -> Dict:
        """Get overall network health"""
        active_sensors = sum(1 for s in self.sensors.values() if s.status == SensorStatus.ACTIVE)
        faulty_sensors = sum(1 for s in self.sensors.values() if s.status == SensorStatus.FAULTY)
        low_battery_sensors = sum(1 for s in self.sensors.values() if s.battery_level < 20)
        
        return {
            'total_sensors': len(self.sensors),
            'active_sensors': active_sensors,
            'faulty_sensors': faulty_sensors,
            'low_battery_sensors': low_battery_sensors,
            'network_health_percentage': round((active_sensors / len(self.sensors)) * 100, 2),
            'total_readings': len(self.all_readings),
            'active_alerts': len([a for a in self.all_alerts if not a.resolved])
        }
    
    def get_sensor_status_report(self) -> Dict:
        """Get detailed sensor status report"""
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'network_health': self.get_network_health(),
            'sensor_details': [sensor.get_health_status() for sensor in self.sensors.values()],
            'recent_alerts': [alert.to_dict() for alert in self.all_alerts[-10:]]  # Last 10 alerts
        }
        return report
    
    def export_readings(self, filename: str):
        """Export all sensor readings to JSON"""
        data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'total_readings': len(self.all_readings),
            'readings': [reading.to_dict() for reading in self.all_readings[-100:]],  # Last 100 readings
            'alerts': [alert.to_dict() for alert in self.all_alerts],
            'network_health': self.get_network_health()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Sensor readings exported to {filename}")


if __name__ == "__main__":
    from smart_parking_system import ParkingLot, SmartParkingSimulator
    
    # Create parking lot
    parking_lot = ParkingLot(lot_name="Downtown Smart Parking", total_slots=120, floors=3)
    
    # Run simulation
    simulator = SmartParkingSimulator(parking_lot)
    simulator.simulate_day_traffic(num_vehicles=80)
    
    # Create sensor network
    sensor_network = SensorNetwork(parking_lot)
    
    # Read all sensors
    for _ in range(5):
        sensor_network.read_all_sensors()
    
    # Get report
    report = sensor_network.get_sensor_status_report()
    print(json.dumps(report, indent=2))
    
    # Export data
    sensor_network.export_readings('/home/ubuntu/sensor_readings.json')
