"""
Smart Parking Analytics and Visualization Module

This module provides comprehensive analytics, reporting, and visualization capabilities
for the Smart Parking Management System.

Author: Internship Project Team
Date: 2024
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
import random
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class ParkingAnalytics:
    """Analytics class for parking system data"""
    
    def __init__(self, parking_lot):
        """Initialize analytics with parking lot data"""
        self.parking_lot = parking_lot
        self.data = None
    
    def load_data(self, json_file: str = None):
        """Load parking data from JSON file"""
        if json_file:
            with open(json_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'lot_name': self.parking_lot.lot_name,
                'total_slots': self.parking_lot.total_slots,
                'floors': self.parking_lot.floors,
                'slots': {slot_id: slot.to_dict() for slot_id, slot in self.parking_lot.slots.items()},
                'vehicles': {v_id: v.to_dict() for v_id, v in self.parking_lot.vehicles.items()},
                'transaction_log': self.parking_lot.transaction_log
            }
    
    def generate_occupancy_heatmap(self, output_file: str = '/home/ubuntu/occupancy_heatmap.png'):
        """Generate occupancy heatmap by floor and section"""
        floor_stats = self.parking_lot.get_floor_occupancy()
        section_stats = self.parking_lot.get_section_occupancy()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Floor occupancy bar chart
        floors = list(floor_stats.keys())
        occupancy_rates = [floor_stats[f]['occupancy_rate'] for f in floors]
        occupied_counts = [floor_stats[f]['occupied_slots'] for f in floors]
        total_counts = [floor_stats[f]['total_slots'] for f in floors]
        
        x_pos = np.arange(len(floors))
        bars1 = ax1.bar(x_pos - 0.2, occupied_counts, 0.4, label='Occupied', color='#FF6B6B', alpha=0.8)
        bars2 = ax1.bar(x_pos + 0.2, [t - o for t, o in zip(total_counts, occupied_counts)], 
                        0.4, label='Vacant', color='#4ECDC4', alpha=0.8)
        
        ax1.set_xlabel('Floor', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Number of Slots', fontsize=12, fontweight='bold')
        ax1.set_title('Parking Occupancy by Floor', fontsize=14, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(floors)
        ax1.legend(fontsize=10)
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        # Section occupancy
        sections = list(section_stats.keys())
        section_occupancy = [section_stats[s]['occupancy_rate'] for s in sections]
        
        colors = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(sections)))
        bars = ax2.barh(sections, section_occupancy, color=colors, alpha=0.8)
        
        ax2.set_xlabel('Occupancy Rate (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Parking Occupancy by Section', fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 100)
        ax2.grid(axis='x', alpha=0.3)
        
        # Add percentage labels
        for i, (bar, rate) in enumerate(zip(bars, section_occupancy)):
            ax2.text(rate + 2, i, f'{rate:.1f}%', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Occupancy heatmap saved to {output_file}")
        plt.close()
    
    def generate_vehicle_type_distribution(self, output_file: str = '/home/ubuntu/vehicle_distribution.png'):
        """Generate vehicle type distribution chart"""
        stats = self.parking_lot.get_occupancy_statistics()
        vehicle_types = stats['vehicles_by_type']
        
        if not vehicle_types:
            logger.warning("No vehicle type data available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Pie chart
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        wedges, texts, autotexts = ax1.pie(vehicle_types.values(), labels=vehicle_types.keys(),
                                            autopct='%1.1f%%', colors=colors, startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('Vehicle Type Distribution (Occupied Slots)', fontsize=14, fontweight='bold')
        
        # Bar chart
        types = list(vehicle_types.keys())
        counts = list(vehicle_types.values())
        bars = ax2.bar(types, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax2.set_ylabel('Number of Vehicles', fontsize=12, fontweight='bold')
        ax2.set_title('Vehicle Count by Type', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add count labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(count)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Vehicle distribution chart saved to {output_file}")
        plt.close()
    
    def generate_occupancy_timeline(self, output_file: str = '/home/ubuntu/occupancy_timeline.png'):
        """Generate occupancy timeline showing changes throughout the day"""
        # Simulate hourly occupancy data
        hours = np.arange(0, 24, 1)
        occupancy_rates = []
        
        for hour in hours:
            # Simulate realistic parking patterns
            if hour < 6:
                rate = random.uniform(5, 15)
            elif hour < 9:
                rate = random.uniform(60, 85)  # Morning rush
            elif hour < 12:
                rate = random.uniform(50, 75)
            elif hour < 14:
                rate = random.uniform(75, 95)  # Lunch time
            elif hour < 17:
                rate = random.uniform(60, 80)
            elif hour < 19:
                rate = random.uniform(70, 90)  # Evening rush
            else:
                rate = random.uniform(20, 50)
            
            occupancy_rates.append(rate)
        
        fig, ax = plt.subplots(figsize=(16, 7))
        
        # Plot line
        ax.plot(hours, occupancy_rates, marker='o', linewidth=3, markersize=8,
                color='#2E86AB', label='Occupancy Rate')
        
        # Fill area under curve
        ax.fill_between(hours, occupancy_rates, alpha=0.3, color='#2E86AB')
        
        # Add threshold lines
        ax.axhline(y=80, color='#FF6B6B', linestyle='--', linewidth=2, label='High Occupancy (80%)', alpha=0.7)
        ax.axhline(y=50, color='#FFD93D', linestyle='--', linewidth=2, label='Medium Occupancy (50%)', alpha=0.7)
        
        ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
        ax.set_ylabel('Occupancy Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Parking Lot Occupancy Throughout the Day', fontsize=14, fontweight='bold')
        ax.set_xticks(hours)
        ax.set_xticklabels([f'{int(h):02d}:00' for h in hours], rotation=45)
        ax.set_ylim(0, 100)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Occupancy timeline saved to {output_file}")
        plt.close()
    
    def generate_revenue_analysis(self, output_file: str = '/home/ubuntu/revenue_analysis.png'):
        """Generate revenue analysis charts"""
        # Simulate daily revenue data
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_revenue = [450 + random.randint(-100, 200) for _ in days]
        daily_vehicles = [85 + random.randint(-20, 40) for _ in days]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Daily revenue bar chart
        colors_revenue = ['#FF6B6B' if r < 400 else '#4ECDC4' if r < 600 else '#45B7D1' for r in daily_revenue]
        bars1 = ax1.bar(days, daily_revenue, color=colors_revenue, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax1.set_ylabel('Revenue ($)', fontsize=12, fontweight='bold')
        ax1.set_title('Daily Parking Revenue', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, revenue in zip(bars1, daily_revenue):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'${int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Vehicles processed
        bars2 = ax2.bar(days, daily_vehicles, color='#A8E6CF', alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax2.set_ylabel('Number of Vehicles', fontsize=12, fontweight='bold')
        ax2.set_title('Daily Vehicle Count', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, vehicles in zip(bars2, daily_vehicles):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Revenue analysis saved to {output_file}")
        plt.close()
    
    def generate_slot_status_distribution(self, output_file: str = '/home/ubuntu/slot_status.png'):
        """Generate slot status distribution chart"""
        stats = self.parking_lot.get_occupancy_statistics()
        
        status_data = {
            'Occupied': stats['occupied_slots'],
            'Vacant': stats['vacant_slots'],
            'Reserved': stats['reserved_slots'],
            'Maintenance': stats['maintenance_slots']
        }
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Pie chart
        colors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#A0A0A0']
        explode = (0.05, 0.05, 0, 0)
        wedges, texts, autotexts = ax1.pie(status_data.values(), labels=status_data.keys(),
                                            autopct='%1.1f%%', colors=colors, explode=explode,
                                            startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('Parking Slot Status Distribution', fontsize=14, fontweight='bold')
        
        # Stacked bar chart
        statuses = list(status_data.keys())
        values = list(status_data.values())
        
        ax2.barh(['Parking Lot'], [stats['total_slots']], color='#E0E0E0', label='Total Slots')
        
        left = 0
        for status, value, color in zip(statuses, values, colors):
            ax2.barh(['Parking Lot'], [value], left=left, color=color, label=status, alpha=0.8)
            # Add label
            ax2.text(left + value/2, 0, f'{value}\n({value/stats["total_slots"]*100:.1f}%)',
                    ha='center', va='center', fontsize=10, fontweight='bold', color='white')
            left += value
        
        ax2.set_xlim(0, stats['total_slots'])
        ax2.set_title('Slot Status Breakdown', fontsize=14, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        ax2.set_xlabel('Number of Slots', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Slot status distribution saved to {output_file}")
        plt.close()
    
    def generate_performance_metrics(self, output_file: str = '/home/ubuntu/performance_metrics.png'):
        """Generate key performance metrics dashboard"""
        stats = self.parking_lot.get_occupancy_statistics()
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
        
        # KPI boxes
        kpis = [
            ('Total Slots', stats['total_slots'], '#2E86AB'),
            ('Occupied', stats['occupied_slots'], '#FF6B6B'),
            ('Vacant', stats['vacant_slots'], '#4ECDC4'),
            ('Occupancy Rate', f"{stats['occupancy_rate']:.1f}%", '#FFD93D'),
            ('Reserved', stats['reserved_slots'], '#A8E6CF'),
            ('Maintenance', stats['maintenance_slots'], '#A0A0A0'),
        ]
        
        for idx, (title, value, color) in enumerate(kpis):
            ax = fig.add_subplot(gs[idx // 3, idx % 3])
            ax.add_patch(mpatches.FancyBboxPatch((0.05, 0.2), 0.9, 0.6,
                                                boxstyle="round,pad=0.05", 
                                                edgecolor=color, facecolor=color, alpha=0.2, linewidth=2))
            ax.text(0.5, 0.65, title, ha='center', va='center', fontsize=12, fontweight='bold')
            ax.text(0.5, 0.35, str(value), ha='center', va='center', fontsize=24, fontweight='bold', color=color)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        # Summary text
        ax_summary = fig.add_subplot(gs[2, :])
        summary_text = f"""
        PARKING LOT: {self.parking_lot.lot_name} | FLOORS: {self.parking_lot.floors} | TOTAL CAPACITY: {stats['total_slots']} slots
        
        Current Status: {stats['occupied_slots']} occupied | {stats['vacant_slots']} vacant | Occupancy Rate: {stats['occupancy_rate']:.1f}%
        
        Vehicle Distribution: {', '.join([f"{k}: {v}" for k, v in stats['vehicles_by_type'].items()])}
        """
        ax_summary.text(0.05, 0.5, summary_text, fontsize=11, verticalalignment='center',
                       family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax_summary.axis('off')
        
        fig.suptitle('Smart Parking Management System - Performance Metrics Dashboard', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Performance metrics dashboard saved to {output_file}")
        plt.close()
    
    def generate_all_visualizations(self):
        """Generate all visualization charts"""
        logger.info("Generating all visualization charts...")
        self.generate_occupancy_heatmap()
        self.generate_vehicle_type_distribution()
        self.generate_occupancy_timeline()
        self.generate_revenue_analysis()
        self.generate_slot_status_distribution()
        self.generate_performance_metrics()
        logger.info("All visualizations generated successfully!")


if __name__ == "__main__":
    from smart_parking_system import ParkingLot, SmartParkingSimulator
    
    # Create parking lot
    parking_lot = ParkingLot(lot_name="Downtown Smart Parking", total_slots=120, floors=3)
    
    # Run simulation
    simulator = SmartParkingSimulator(parking_lot)
    simulator.simulate_day_traffic(num_vehicles=100)
    
    # Generate analytics
    analytics = ParkingAnalytics(parking_lot)
    analytics.generate_all_visualizations()
    
    print("Analytics generation completed!")
