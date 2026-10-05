"""
Real-Time Smart Parking Management System with IoT-Based Vehicle Slot Detection
Main Module: Smart Parking System Simulation and Analytics

This module implements a comprehensive IoT-based parking management system that simulates
real-time vehicle detection, occupancy monitoring, and analytics generation.

Author: Internship Project Team
Date: 2024
"""

import json
import random
import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SlotStatus(Enum):
    """Enumeration for parking slot status"""
    VACANT = "Vacant"
    OCCUPIED = "Occupied"
    RESERVED = "Reserved"
    MAINTENANCE = "Maintenance"


class VehicleType(Enum):
    """Enumeration for vehicle types"""
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"
    TRUCK = "Truck"
    HANDICAP = "Handicap"


@dataclass
class ParkingSlot:
    """Data class representing a parking slot"""
    slot_id: str
    floor: int
    section: str
    status: SlotStatus
    vehicle_type: VehicleType
    occupancy_time: datetime.datetime = None
    sensor_reading: float = 0.0  # Distance reading from ultrasonic sensor (cm)
    last_updated: datetime.datetime = None
    
    def to_dict(self):
        """Convert slot to dictionary"""
        return {
            'slot_id': self.slot_id,
            'floor': self.floor,
            'section': self.section,
            'status': self.status.value,
            'vehicle_type': self.vehicle_type.value,
            'occupancy_time': self.occupancy_time.isoformat() if self.occupancy_time else None,
            'sensor_reading': self.sensor_reading,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }


@dataclass
class Vehicle:
    """Data class representing a vehicle"""
    vehicle_id: str
    vehicle_type: VehicleType
    entry_time: datetime.datetime
    exit_time: datetime.datetime = None
    slot_id: str = None
    parking_duration: int = 0  # in minutes
    
    def to_dict(self):
        """Convert vehicle to dictionary"""
        return {
            'vehicle_id': self.vehicle_id,
            'vehicle_type': self.vehicle_type.value,
            'entry_time': self.entry_time.isoformat(),
            'exit_time': self.exit_time.isoformat() if self.exit_time else None,
            'slot_id': self.slot_id,
            'parking_duration': self.parking_duration
        }


@dataclass
class ParkingAlert:
    """Data class representing a parking system alert"""
    alert_id: str
    alert_type: str  # 'FULL', 'LOW_AVAILABILITY', 'SENSOR_FAILURE', 'UNAUTHORIZED_ENTRY'
    severity: str  # 'INFO', 'WARNING', 'CRITICAL'
    message: str
    timestamp: datetime.datetime
    resolved: bool = False
    
    def to_dict(self):
        """Convert alert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved
        }


class ParkingLot:
    """Main class for managing a parking lot"""
    
    def __init__(self, lot_name: str, total_slots: int, floors: int = 3):
        """
        Initialize a parking lot
        
        Args:
            lot_name: Name of the parking lot
            total_slots: Total number of parking slots
            floors: Number of floors in the parking lot
        """
        self.lot_name = lot_name
        self.total_slots = total_slots
        self.floors = floors
        self.slots_per_floor = total_slots // floors
        self.slots: Dict[str, ParkingSlot] = {}
        self.vehicles: Dict[str, Vehicle] = {}
        self.alerts: List[ParkingAlert] = []
        self.transaction_log: List[Dict] = []
        
        self._initialize_slots()
        logger.info(f"Parking lot '{lot_name}' initialized with {total_slots} slots across {floors} floors")
    
    def _initialize_slots(self):
        """Initialize all parking slots"""
        slot_counter = 1
        sections = ['A', 'B', 'C', 'D']
        
        for floor in range(1, self.floors + 1):
            slots_in_floor = self.slots_per_floor
            for i in range(slots_in_floor):
                section = sections[i % len(sections)]
                slot_id = f"F{floor}{section}{(i // len(sections)) + 1}"
                
                # Assign vehicle types to slots
                if slot_counter % 10 == 0:
                    vehicle_type = VehicleType.HANDICAP
                elif slot_counter % 8 == 0:
                    vehicle_type = VehicleType.TRUCK
                elif slot_counter % 5 == 0:
                    vehicle_type = VehicleType.MOTORCYCLE
                else:
                    vehicle_type = VehicleType.CAR
                
                slot = ParkingSlot(
                    slot_id=slot_id,
                    floor=floor,
                    section=section,
                    status=SlotStatus.VACANT,
                    vehicle_type=vehicle_type,
                    last_updated=datetime.datetime.now()
                )
                self.slots[slot_id] = slot
                slot_counter += 1
    
    def vehicle_entry(self, vehicle_id: str, vehicle_type: VehicleType) -> Tuple[bool, str]:
        """
        Process vehicle entry into the parking lot
        
        Args:
            vehicle_id: Unique identifier for the vehicle
            vehicle_type: Type of vehicle
            
        Returns:
            Tuple of (success: bool, message: str, slot_id: str or None)
        """
        # Check if parking lot is full
        available_slots = self.get_available_slots(vehicle_type)
        
        if not available_slots:
            alert = ParkingAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                alert_type="FULL",
                severity="CRITICAL",
                message=f"Parking lot is full. No available slots for {vehicle_type.value}",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.warning(f"Parking lot full - Vehicle {vehicle_id} cannot be parked")
            return False, "Parking lot is full", None
        
        # Assign the first available slot
        slot = available_slots[0]
        slot.status = SlotStatus.OCCUPIED
        slot.occupancy_time = datetime.datetime.now()
        slot.sensor_reading = 5.0  # Sensor detects vehicle (short distance)
        slot.last_updated = datetime.datetime.now()
        
        # Create vehicle record
        vehicle = Vehicle(
            vehicle_id=vehicle_id,
            vehicle_type=vehicle_type,
            entry_time=datetime.datetime.now(),
            slot_id=slot.slot_id
        )
        self.vehicles[vehicle_id] = vehicle
        
        # Log transaction
        self.transaction_log.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'event': 'ENTRY',
            'vehicle_id': vehicle_id,
            'vehicle_type': vehicle_type.value,
            'slot_id': slot.slot_id,
            'status': 'SUCCESS'
        })
        
        logger.info(f"Vehicle {vehicle_id} parked in slot {slot.slot_id}")
        return True, f"Vehicle parked successfully in slot {slot.slot_id}", slot.slot_id
    
    def vehicle_exit(self, vehicle_id: str) -> Tuple[bool, str, float]:
        """
        Process vehicle exit from the parking lot
        
        Args:
            vehicle_id: Unique identifier for the vehicle
            
        Returns:
            Tuple of (success: bool, message: str, parking_fee: float)
        """
        if vehicle_id not in self.vehicles:
            logger.error(f"Vehicle {vehicle_id} not found in system")
            return False, "Vehicle not found in system", 0.0
        
        vehicle = self.vehicles[vehicle_id]
        slot = self.slots[vehicle.slot_id]
        
        # Calculate parking duration and fee
        exit_time = datetime.datetime.now()
        duration_minutes = (exit_time - vehicle.entry_time).total_seconds() / 60
        vehicle.parking_duration = int(duration_minutes)
        vehicle.exit_time = exit_time
        
        # Calculate parking fee (simplified: $2 per hour)
        parking_fee = (duration_minutes / 60) * 2.0
        
        # Update slot status
        slot.status = SlotStatus.VACANT
        slot.sensor_reading = 200.0  # Sensor detects no vehicle (far distance)
        slot.last_updated = datetime.datetime.now()
        slot.occupancy_time = None
        
        # Log transaction
        self.transaction_log.append({
            'timestamp': exit_time.isoformat(),
            'event': 'EXIT',
            'vehicle_id': vehicle_id,
            'vehicle_type': vehicle.vehicle_type.value,
            'slot_id': vehicle.slot_id,
            'parking_duration_minutes': vehicle.parking_duration,
            'parking_fee': round(parking_fee, 2),
            'status': 'SUCCESS'
        })
        
        logger.info(f"Vehicle {vehicle_id} exited from slot {vehicle.slot_id}. Duration: {vehicle.parking_duration} min, Fee: ${parking_fee:.2f}")
        return True, f"Vehicle exited successfully", parking_fee
    
    def get_available_slots(self, vehicle_type: VehicleType = None) -> List[ParkingSlot]:
        """
        Get list of available parking slots
        
        Args:
            vehicle_type: Filter by vehicle type (optional)
            
        Returns:
            List of available slots
        """
        available = []
        for slot in self.slots.values():
            if slot.status == SlotStatus.VACANT:
                if vehicle_type is None or slot.vehicle_type == vehicle_type:
                    available.append(slot)
        return available
    
    def get_occupancy_statistics(self) -> Dict:
        """
        Get parking lot occupancy statistics
        
        Returns:
            Dictionary containing occupancy statistics
        """
        total = len(self.slots)
        occupied = sum(1 for slot in self.slots.values() if slot.status == SlotStatus.OCCUPIED)
        vacant = sum(1 for slot in self.slots.values() if slot.status == SlotStatus.VACANT)
        reserved = sum(1 for slot in self.slots.values() if slot.status == SlotStatus.RESERVED)
        maintenance = sum(1 for slot in self.slots.values() if slot.status == SlotStatus.MAINTENANCE)
        
        occupancy_rate = (occupied / total * 100) if total > 0 else 0
        
        # Count by vehicle type
        vehicle_type_count = {}
        for slot in self.slots.values():
            if slot.status == SlotStatus.OCCUPIED:
                vtype = slot.vehicle_type.value
                vehicle_type_count[vtype] = vehicle_type_count.get(vtype, 0) + 1
        
        return {
            'total_slots': total,
            'occupied_slots': occupied,
            'vacant_slots': vacant,
            'reserved_slots': reserved,
            'maintenance_slots': maintenance,
            'occupancy_rate': round(occupancy_rate, 2),
            'vehicles_by_type': vehicle_type_count
        }
    
    def get_floor_occupancy(self) -> Dict:
        """
        Get occupancy statistics by floor
        
        Returns:
            Dictionary containing occupancy by floor
        """
        floor_stats = {}
        for floor in range(1, self.floors + 1):
            floor_slots = [s for s in self.slots.values() if s.floor == floor]
            occupied = sum(1 for s in floor_slots if s.status == SlotStatus.OCCUPIED)
            total = len(floor_slots)
            occupancy_rate = (occupied / total * 100) if total > 0 else 0
            
            floor_stats[f"Floor {floor}"] = {
                'total_slots': total,
                'occupied_slots': occupied,
                'vacant_slots': total - occupied,
                'occupancy_rate': round(occupancy_rate, 2)
            }
        
        return floor_stats
    
    def get_section_occupancy(self) -> Dict:
        """
        Get occupancy statistics by section
        
        Returns:
            Dictionary containing occupancy by section
        """
        section_stats = {}
        sections = set(slot.section for slot in self.slots.values())
        
        for section in sorted(sections):
            section_slots = [s for s in self.slots.values() if s.section == section]
            occupied = sum(1 for s in section_slots if s.status == SlotStatus.OCCUPIED)
            total = len(section_slots)
            occupancy_rate = (occupied / total * 100) if total > 0 else 0
            
            section_stats[f"Section {section}"] = {
                'total_slots': total,
                'occupied_slots': occupied,
                'vacant_slots': total - occupied,
                'occupancy_rate': round(occupancy_rate, 2)
            }
        
        return section_stats
    
    def generate_hourly_report(self) -> Dict:
        """
        Generate hourly parking report
        
        Returns:
            Dictionary containing hourly statistics
        """
        stats = self.get_occupancy_statistics()
        floor_stats = self.get_floor_occupancy()
        section_stats = self.get_section_occupancy()
        
        # Calculate revenue from transactions
        total_revenue = 0.0
        total_vehicles_processed = 0
        
        for transaction in self.transaction_log:
            if transaction['event'] == 'EXIT':
                total_revenue += transaction.get('parking_fee', 0)
                total_vehicles_processed += 1
        
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'lot_name': self.lot_name,
            'overall_statistics': stats,
            'floor_statistics': floor_stats,
            'section_statistics': section_stats,
            'total_vehicles_processed': total_vehicles_processed,
            'total_revenue': round(total_revenue, 2),
            'active_alerts': len([a for a in self.alerts if not a.resolved])
        }
        
        return report
    
    def export_to_json(self, filename: str):
        """Export parking lot data to JSON file"""
        data = {
            'lot_name': self.lot_name,
            'total_slots': self.total_slots,
            'floors': self.floors,
            'slots': {slot_id: slot.to_dict() for slot_id, slot in self.slots.items()},
            'vehicles': {v_id: v.to_dict() for v_id, v in self.vehicles.items()},
            'alerts': [alert.to_dict() for alert in self.alerts],
            'transaction_log': self.transaction_log
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Data exported to {filename}")


class SmartParkingSimulator:
    """Simulator for generating realistic parking scenarios"""
    
    def __init__(self, parking_lot: ParkingLot):
        """Initialize simulator"""
        self.parking_lot = parking_lot
        self.vehicle_counter = 0
    
    def simulate_day_traffic(self, num_vehicles: int = 150, simulation_hours: int = 8):
        """
        Simulate a day's worth of parking traffic
        
        Args:
            num_vehicles: Number of vehicles to simulate
            simulation_hours: Duration of simulation in hours
        """
        logger.info(f"Starting simulation with {num_vehicles} vehicles over {simulation_hours} hours")
        
        # Vehicle entry phase
        entry_times = []
        for i in range(num_vehicles):
            vehicle_id = f"VEH_{self.vehicle_counter:05d}"
            self.vehicle_counter += 1
            
            # Random vehicle type
            vehicle_type = random.choice(list(VehicleType))
            
            # Simulate entry
            success, message, slot_id = self.parking_lot.vehicle_entry(vehicle_id, vehicle_type)
            
            if success:
                entry_times.append((vehicle_id, slot_id))
            else:
                logger.warning(f"Failed to park vehicle {vehicle_id}")
        
        logger.info(f"Successfully parked {len(entry_times)} vehicles")
        
        # Vehicle exit phase (simulate after random duration)
        for vehicle_id, slot_id in entry_times:
            # Random parking duration between 30 minutes to 4 hours
            duration_minutes = random.randint(30, 240)
            
            # Simulate exit
            success, message, fee = self.parking_lot.vehicle_exit(vehicle_id)
            
            if success:
                logger.info(f"Vehicle {vehicle_id} exited. Fee: ${fee:.2f}")
    
    def get_simulation_report(self) -> Dict:
        """Get comprehensive simulation report"""
        return self.parking_lot.generate_hourly_report()


if __name__ == "__main__":
    # Create parking lot
    parking_lot = ParkingLot(lot_name="Downtown Smart Parking", total_slots=120, floors=3)
    
    # Create simulator
    simulator = SmartParkingSimulator(parking_lot)
    
    # Run simulation
    simulator.simulate_day_traffic(num_vehicles=100, simulation_hours=8)
    
    # Generate report
    report = simulator.get_simulation_report()
    
    # Print report
    print("\n" + "="*60)
    print("SMART PARKING MANAGEMENT SYSTEM - SIMULATION REPORT")
    print("="*60)
    print(json.dumps(report, indent=2))
    
    # Export data
    parking_lot.export_to_json('/home/ubuntu/parking_data.json')
