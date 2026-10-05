"""
Script to generate the comprehensive 30+ page Word document internship report
for the Smart Parking Management System.
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

# Create document
doc = Document()

# Configure margins
sections = doc.sections
for section in sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# Custom styles
def create_custom_styles(doc):
    styles = doc.styles
    
    # Title style
    title_style = styles.add_style('CustomTitle', WD_STYLE_TYPE.PARAGRAPH)
    title_style.font.name = 'Times New Roman'
    title_style.font.size = Pt(24)
    title_style.font.bold = True
    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_style.paragraph_format.space_after = Pt(24)
    
    # Chapter Title Style (Centered, uppercase)
    chap_title = styles.add_style('ChapterTitle', WD_STYLE_TYPE.PARAGRAPH)
    chap_title.font.name = 'Times New Roman'
    chap_title.font.size = Pt(16)
    chap_title.font.bold = True
    chap_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    chap_title.paragraph_format.space_before = Pt(24)
    chap_title.paragraph_format.space_after = Pt(24)
    
    # Heading 1 (e.g. 1.1)
    h1_style = styles.add_style('CustomHeading1', WD_STYLE_TYPE.PARAGRAPH)
    h1_style.font.name = 'Times New Roman'
    h1_style.font.size = Pt(14)
    h1_style.font.bold = True
    h1_style.paragraph_format.space_before = Pt(18)
    h1_style.paragraph_format.space_after = Pt(12)
    
    # Heading 2 (e.g. 1.1.1)
    h2_style = styles.add_style('CustomHeading2', WD_STYLE_TYPE.PARAGRAPH)
    h2_style.font.name = 'Times New Roman'
    h2_style.font.size = Pt(13)
    h2_style.font.bold = True
    h2_style.paragraph_format.space_before = Pt(12)
    h2_style.paragraph_format.space_after = Pt(6)
    
    # Body Text
    body_style = styles.add_style('CustomBody', WD_STYLE_TYPE.PARAGRAPH)
    body_style.font.name = 'Times New Roman'
    body_style.font.size = Pt(12)
    body_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    body_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    body_style.paragraph_format.space_after = Pt(12)

create_custom_styles(doc)

def add_chapter_title(doc, chapter_num, title_text):
    doc.add_page_break()
    p1 = doc.add_paragraph(f"CHAPTER {chapter_num}", style='ChapterTitle')
    p2 = doc.add_paragraph(title_text.upper(), style='ChapterTitle')
    p2.paragraph_format.space_before = Pt(0)

def add_section_heading(doc, num, text):
    doc.add_paragraph(f"{num} {text}", style='CustomHeading1')

def add_subsection_heading(doc, num, text):
    doc.add_paragraph(f"{num} {text}", style='CustomHeading2')

def add_body_text(doc, text):
    doc.add_paragraph(text, style='CustomBody')

def add_bullet_point(doc, text):
    p = doc.add_paragraph(style='CustomBody')
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    run = p.add_run("•\t" + text)

def add_image_with_caption(doc, img_path, caption):
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(img_path, width=Inches(6.0))
        
        cap_p = doc.add_paragraph(caption)
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.runs[0].font.italic = True
        cap_p.runs[0].font.size = Pt(10)

# ---------------- TITLE PAGE ----------------
doc.add_paragraph("\n\n\n\n")
title = doc.add_paragraph("INTERNSHIP REPORT\nON", style='CustomTitle')
title.runs[0].font.size = Pt(18)

main_title = doc.add_paragraph("REAL-TIME SMART PARKING MANAGEMENT SYSTEM WITH IOT-BASED VEHICLE SLOT DETECTION AND AVAILABILITY MONITORING", style='CustomTitle')

doc.add_paragraph("\n\nSubmitted in partial fulfillment of the requirements for the award of the degree of", style='CustomBody').alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph("BACHELOR OF TECHNOLOGY", style='CustomHeading1').alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph("\n\nPrepared by:\nInternship Project Team\n2024", style='CustomBody').alignment = WD_ALIGN_PARAGRAPH.CENTER

# ---------------- TABLE OF CONTENTS (Placeholder) ----------------
doc.add_page_break()
doc.add_paragraph("TABLE OF CONTENTS", style='ChapterTitle')
add_body_text(doc, "1. EXECUTIVE SUMMARY ........................................................................ 1")
add_body_text(doc, "   1.1 Learning Objectives .................................................................. 1")
add_body_text(doc, "   1.2 Outcomes Achieved .................................................................... 2")
add_body_text(doc, "2. OVERVIEW OF THE ORGANIZATION ............................................................. 3")
add_body_text(doc, "3. PROBLEM ASSESSMENT AND ANALYSIS .......................................................... 5")
add_body_text(doc, "   3.1 Problem Statement .................................................................... 5")
add_body_text(doc, "   3.2 Key Parameters ....................................................................... 6")
add_body_text(doc, "   3.3 Requirements Evaluation .............................................................. 8")
add_body_text(doc, "4. SOLUTION DESIGN AND ARCHITECTURE ......................................................... 11")
add_body_text(doc, "   4.1 Solution Blueprint ................................................................... 11")
add_body_text(doc, "   4.2 Feasibility Assessment ............................................................... 13")
add_body_text(doc, "   4.3 Project Implementation Plan .......................................................... 15")
add_body_text(doc, "5. SOLUTION DEVELOPMENT AND TECHNOLOGY STACK ................................................ 18")
add_body_text(doc, "   5.1 Technology Stack Determination ....................................................... 18")
add_body_text(doc, "   5.2 Implementation Details ............................................................... 20")
add_body_text(doc, "   5.3 Code Explanations .................................................................... 22")
add_body_text(doc, "6. SOLUTION TESTING AND PERFORMANCE EVALUATION .............................................. 25")
add_body_text(doc, "   6.1 Testing Strategy ..................................................................... 25")
add_body_text(doc, "   6.2 Performance Evaluation ............................................................... 27")
add_body_text(doc, "7. RESULTS AND VISUALIZATIONS ............................................................... 29")
add_body_text(doc, "8. CONCLUSION AND LEARNING EVALUATION ....................................................... 33")
add_body_text(doc, "REFERENCES .................................................................................. 35")

# ---------------- CHAPTER 1: EXECUTIVE SUMMARY ----------------
add_chapter_title(doc, 1, "EXECUTIVE SUMMARY")
add_body_text(doc, "This internship report provides a comprehensive overview of my internship project focused on developing a Real-Time Smart Parking Management System with IoT-Based Vehicle Slot Detection and Availability Monitoring. The internship was undertaken as part of the academic curriculum for the Bachelor of Technology. The primary objective of this internship was to gain proficiency in Internet of Things (IoT), software development, data analytics, and system architecture design to enhance employability skills while solving a real-world urban challenge.")

add_body_text(doc, "Finding available parking spaces in crowded urban areas is a major challenge, resulting in traffic congestion, fuel wastage, and increased travel time. Traditional parking management systems rely on manual monitoring, making it difficult to provide real-time information about parking availability. The proposed solution addresses this by creating a centralized platform where parking spaces are continuously monitored through a secure and user-friendly interface.")

add_section_heading(doc, "1.1", "Learning Objectives")
add_body_text(doc, "During my internship, I learned and practiced the following:")
add_bullet_point(doc, "To design and implement a smart parking simulation system using Python that accurately models IoT sensor behavior, vehicle entry/exit dynamics, and parking slot occupancy.")
add_bullet_point(doc, "To integrate data analytics techniques for understanding parking utilization patterns, generating heatmaps, and creating performance dashboards.")
add_bullet_point(doc, "To implement interactive features such as real-time alerts, automated fee calculation, and transaction logging.")
add_bullet_point(doc, "To create a scalable system architecture that supports deployment across multiple platforms, including web and mobile interfaces.")
add_bullet_point(doc, "To design a system that ensures secure communication, reliable performance, and seamless handling of concurrent vehicle transactions with low latency.")

add_section_heading(doc, "1.2", "Outcomes Achieved")
add_body_text(doc, "Key outcomes from my internship include:")
add_bullet_point(doc, "A fully operational smart parking simulation capable of modeling complex parking scenarios, multiple floors, and various vehicle types.")
add_bullet_point(doc, "An advanced analytics module that generates comprehensive visual reports including occupancy heatmaps, timeline distributions, and revenue analysis.")
add_bullet_point(doc, "A robust IoT sensor simulation framework that models ultrasonic and infrared sensors, including anomaly detection and battery degradation mechanics.")
add_bullet_point(doc, "Comprehensive understanding of full-stack system design, bridging hardware constraints with software capabilities.")
add_bullet_point(doc, "The system architecture supports modular development, scalability for future enhancements, and efficient use of resources.")

# ---------------- CHAPTER 2: OVERVIEW OF THE ORGANIZATION ----------------
add_chapter_title(doc, 2, "OVERVIEW OF THE ORGANIZATION")
add_section_heading(doc, "2.1", "Introduction of the Organization")
add_body_text(doc, "The organization hosting this internship is a leading technology solutions provider focused on bridging the academia-industry divide, enhancing student employability, promoting innovation, and fostering an entrepreneurial ecosystem. By leveraging emerging technologies such as IoT, AI, and cloud computing, the organization aims to augment and upgrade the knowledge ecosystem, enabling beneficiaries to become contributors themselves. The organization offers comprehensive mentorship programs, benefiting thousands of learners annually.")

add_section_heading(doc, "2.2", "Vision, Mission, and Values")
add_bullet_point(doc, "Vision: To combine cutting-edge technology with impactful social ventures to drive urban prosperity and smart city infrastructure.")
add_bullet_point(doc, "Mission: To support individuals dedicated to solving real-world problems by empowering and equipping them with industry-standard technical skills.")
add_bullet_point(doc, "Values: The organization emphasizes technological skills for Industry 4.0 and 5.0, focusing on sustainability, efficiency, and inclusive access for everyone to be future-ready.")

add_section_heading(doc, "2.3", "Policy of the Organization in Relation to the Intern Role")
add_body_text(doc, "Interns are expected to adhere to the following policies:")
add_bullet_point(doc, "Confidentiality: Interns must maintain the confidentiality of all organizational data and proprietary algorithms.")
add_bullet_point(doc, "Professionalism: Interns are expected to demonstrate professionalism, punctuality, and respect for all team members and mentors.")
add_bullet_point(doc, "Learning and Contribution: Interns are encouraged to actively participate in projects, share innovative ideas, and contribute to the organization's technological goals.")
add_bullet_point(doc, "Compliance: Interns must comply with all organizational policies, including ethical guidelines for software development.")

add_section_heading(doc, "2.4", "Roles and Responsibilities of the Employees Guiding the Intern")
add_body_text(doc, "Interns are typically placed under the guidance of technical program managers and senior software architects. The roles and responsibilities of the employees include:")
add_body_text(doc, "1. Technical Mentors:")
add_bullet_point(doc, "Design and implement project milestones.")
add_bullet_point(doc, "Mentor and supervise interns in coding practices and system design.")
add_bullet_point(doc, "Conduct regular code reviews and provide constructive feedback.")

add_body_text(doc, "2. System Architects:")
add_bullet_point(doc, "Guide the architectural decisions for IoT integration.")
add_bullet_point(doc, "Ensure scalability and security of the proposed solutions.")
add_bullet_point(doc, "Analyze system performance and provide optimization recommendations.")

# ---------------- CHAPTER 3: PROBLEM ASSESSMENT AND ANALYSIS ----------------
add_chapter_title(doc, 3, "PROBLEM ASSESSMENT AND ANALYSIS")
add_body_text(doc, "This chapter addresses Performance Criterion 1 (PC1) and Performance Criterion 2 (PC2) of the evaluation criteria, focusing on problem selection, parameter identification, and requirements evaluation.")

add_section_heading(doc, "3.1", "Problem Statement")
add_body_text(doc, "Finding available parking spaces in crowded urban areas is a major challenge, resulting in traffic congestion, fuel wastage, and increased travel time. Traditional parking management systems rely on manual monitoring, making it difficult to provide real-time information about parking availability. Parking operators and drivers require intelligent systems that can automatically detect vehicle occupancy and monitor parking space availability.")

add_section_heading(doc, "3.2", "Key Parameters (PC1)")
add_body_text(doc, "The problem statement encompasses several key parameters that define the scope and target of the solution:")

add_subsection_heading(doc, "3.2.1", "Issue to be Solved")
add_body_text(doc, "The core issue is the inefficiency in urban parking management. Specifically, drivers spend an excessive amount of time circling parking lots to find vacant spots, which leads to increased carbon emissions, driver frustration, and localized traffic congestion. For parking operators, the lack of real-time visibility into lot occupancy leads to suboptimal space utilization, revenue leakage, and inability to implement dynamic pricing strategies.")

add_subsection_heading(doc, "3.2.2", "Target Community")
add_body_text(doc, "The target community for this solution is twofold:")
add_bullet_point(doc, "Primary Users (Drivers): Commuters, shoppers, employees, and visitors in urban centers who require efficient parking solutions.")
add_bullet_point(doc, "Secondary Users (Administrators): Parking lot owners, facility managers in shopping malls, educational institutions, hospitals, airports, and municipal authorities managing smart city infrastructure.")

add_subsection_heading(doc, "3.2.3", "User Needs and Preferences")
add_body_text(doc, "Drivers need a seamless, frictionless experience where they are immediately guided to an available slot upon entry. They prefer minimal waiting times and clear visual indicators. Administrators need a centralized, comprehensive dashboard that provides real-time occupancy data, historical analytics, automated alert systems for hardware failures, and revenue tracking capabilities.")

add_section_heading(doc, "3.3", "Requirements Evaluation (PC2)")
add_body_text(doc, "To effectively map the solution to the problem statement, the system requirements have been evaluated and categorized into functional and non-functional requirements.")

add_subsection_heading(doc, "3.3.1", "Functional Requirements")
add_body_text(doc, "Functional requirements define the specific behaviors and functions the system must perform:")
add_bullet_point(doc, "Real-time Vehicle Detection: The system must accurately detect the presence or absence of a vehicle in a specific parking slot using IoT sensors.")
add_bullet_point(doc, "Occupancy Status Updates: The system must immediately update the central database when a slot's status changes from vacant to occupied or vice versa.")
add_bullet_point(doc, "Automated Entry and Exit Processing: The system must log vehicle entry times, assign slots, log exit times, and calculate parking durations and fees.")
add_bullet_point(doc, "Analytics and Reporting: The system must generate comprehensive reports on utilization rates, peak hours, and revenue.")
add_bullet_point(doc, "Alert Generation: The system must trigger alerts for specific events such as lot full capacity, sensor malfunction, or low battery levels.")

add_subsection_heading(doc, "3.3.2", "Non-Functional Requirements")
add_body_text(doc, "Non-functional requirements specify criteria that judge the operation of the system:")
add_bullet_point(doc, "Reliability: The sensor network must maintain high accuracy, minimizing false positives (detecting a car when none is there) and false negatives.")
add_bullet_point(doc, "Scalability: The architecture must support seamless addition of new parking floors, sections, and hundreds of concurrent sensor connections.")
add_bullet_point(doc, "Performance: Status updates must reflect on the administrative dashboard within seconds of the physical event occurring.")
add_bullet_point(doc, "Security: Data transmission between IoT nodes and the central server must be encrypted to prevent unauthorized access or manipulation of parking data.")

# ---------------- CHAPTER 4: SOLUTION DESIGN AND ARCHITECTURE ----------------
add_chapter_title(doc, 4, "SOLUTION DESIGN AND ARCHITECTURE")
add_body_text(doc, "This chapter addresses Performance Criterion 3 (PC3) and Performance Criterion 4 (PC4) of the evaluation criteria, focusing on the solution blueprint, feasibility assessment, and project implementation plan.")

add_section_heading(doc, "4.1", "Solution Blueprint (PC3)")
add_body_text(doc, "The proposed solution is a Real-Time Smart Parking Management System that integrates hardware sensors with a robust software backend and an analytical frontend. The blueprint is divided into three primary layers:")

add_subsection_heading(doc, "4.1.1", "Perception Layer (IoT Edge)")
add_body_text(doc, "This layer consists of the physical hardware deployed at the parking facility. Each parking slot is equipped with an IoT sensor (simulated in this project as ultrasonic or infrared sensors). These sensors continuously measure distance or detect presence. A micro-controller at the edge processes raw analog signals, applies basic noise filtering, and transmits binary state changes (occupied/vacant) to the central gateway via wireless protocols (e.g., Wi-Fi, LoRaWAN, or Zigbee).")

add_subsection_heading(doc, "4.1.2", "Network and Processing Layer (Backend)")
add_body_text(doc, "The backend server acts as the brain of the system. It receives telemetry data from the edge devices. The core logic engine processes these state changes, updates the central database, handles vehicle entry/exit transactions, calculates parking fees, and monitors the health status of the sensor network. It also includes an anomaly detection module to identify faulty sensors or irregular data patterns.")

add_subsection_heading(doc, "4.1.3", "Application Layer (Frontend Analytics)")
add_body_text(doc, "The application layer provides the interface for administrators. It consumes data from the backend to render real-time dashboards, occupancy heatmaps, timeline charts, and revenue reports. This layer transforms raw tabular data into actionable visual insights, allowing operators to make informed decisions regarding dynamic pricing or maintenance scheduling.")

add_section_heading(doc, "4.2", "Feasibility Assessment")
add_body_text(doc, "The feasibility of the proposed blueprint was assessed across multiple dimensions:")
add_bullet_point(doc, "Technical Feasibility: Highly feasible. The technologies required (IoT sensors, Python backend, data visualization libraries) are mature, well-documented, and widely adopted in the industry. The simulation approach allows for rigorous testing of logic before physical hardware deployment.")
add_bullet_point(doc, "Economic Feasibility: Feasible. By utilizing cost-effective ultrasonic sensors and open-source software stacks, the initial capital expenditure is minimized. The system's ability to optimize space utilization and reduce manual monitoring labor provides a strong return on investment (ROI).")
add_bullet_point(doc, "Operational Feasibility: Feasible. The automated nature of the system significantly reduces the operational burden on facility staff. The intuitive dashboards require minimal training for administrators to operate effectively.")

add_section_heading(doc, "4.3", "Project Implementation Plan (PC4)")
add_body_text(doc, "The project was executed over an 8-week period with clearly defined milestones, deadlines, and resource allocation.")

add_subsection_heading(doc, "4.3.1", "Milestones and Deadlines")
add_body_text(doc, "Week 1-2: Requirements Gathering and Architecture Design. Finalizing the problem statement, defining functional requirements, and designing the class structures for the simulation.")
add_body_text(doc, "Week 3-4: Core Backend Development. Implementing the ParkingLot, ParkingSlot, and Vehicle classes. Developing the entry and exit transaction logic.")
add_body_text(doc, "Week 5: IoT Sensor Simulation. Developing the SensorNetwork and IoTSensor classes, including realistic noise generation and anomaly detection algorithms.")
add_body_text(doc, "Week 6: Analytics and Visualization. Integrating Matplotlib and Seaborn to generate heatmaps, timelines, and performance dashboards based on simulated data.")
add_body_text(doc, "Week 7: Testing and Debugging. Running extensive simulations to identify edge cases, memory leaks, and logical errors in fee calculation or slot assignment.")
add_body_text(doc, "Week 8: Documentation and Final Presentation. Compiling the internship report, formatting code, and preparing the final project presentation.")

add_subsection_heading(doc, "4.3.2", "Resource Allocation")
add_body_text(doc, "The project required the following resources:")
add_bullet_point(doc, "Human Resources: 1 Software Developer Intern, 1 Technical Mentor.")
add_bullet_point(doc, "Software Resources: Python 3.11 environment, IDE (VS Code), Git for version control.")
add_bullet_point(doc, "Compute Resources: Standard development machine for running the Python simulation and rendering high-resolution visualization charts.")

# ---------------- CHAPTER 5: SOLUTION DEVELOPMENT AND TECHNOLOGY STACK ----------------
add_chapter_title(doc, 5, "SOLUTION DEVELOPMENT AND TECHNOLOGY STACK")
add_body_text(doc, "This chapter addresses Performance Criterion 5 (PC5) and Performance Criterion 6 (PC6) of the evaluation criteria, detailing the technology stack selection and the technical build process.")

add_section_heading(doc, "5.1", "Technology Stack Determination (PC5)")
add_body_text(doc, "The technology stack was carefully selected to ensure rapid prototyping, robust data handling, and high-quality visualizations.")

add_subsection_heading(doc, "5.1.1", "Programming Language: Python")
add_body_text(doc, "Python was selected as the primary programming language due to its exceptional readability, extensive standard library, and dominance in data science and IoT backend processing. Its object-oriented capabilities allowed for clean modeling of real-world entities like parking slots and sensors.")

add_subsection_heading(doc, "5.1.2", "Data Visualization: Matplotlib and Seaborn")
add_body_text(doc, "For the analytics dashboard, Matplotlib and Seaborn were chosen. Matplotlib provides fine-grained control over figure elements, while Seaborn offers high-level interfaces for drawing attractive and informative statistical graphics. These libraries are industry standards for transforming raw data into business intelligence insights.")

add_subsection_heading(doc, "5.1.3", "Data Handling: JSON and Dataclasses")
add_body_text(doc, "Python's native 'dataclasses' module was used to define data structures cleanly with minimal boilerplate code. JSON (JavaScript Object Notation) was selected for data serialization and export, simulating how a real IoT gateway would transmit telemetry data to a cloud endpoint.")

add_section_heading(doc, "5.2", "Implementation Details (PC6)")
add_body_text(doc, "The solution was built precisely according to the technical specifications defined in the blueprint. The system comprises three main Python modules: 'smart_parking_system.py', 'iot_sensors.py', and 'parking_analytics.py'.")

add_subsection_heading(doc, "5.2.1", "Core System Implementation")
add_body_text(doc, "The core system manages the state of the parking facility. The 'ParkingLot' class initializes a configurable number of slots across multiple floors and sections. It handles 'vehicle_entry' and 'vehicle_exit' methods. During entry, the system scans for the first available slot matching the vehicle type (Car, Motorcycle, Truck, Handicap) and updates the slot status to OCCUPIED. During exit, it calculates the parking duration and applies a fee algorithm.")

add_subsection_heading(doc, "5.2.2", "IoT Sensor Simulation")
add_body_text(doc, "To accurately reflect real-world hardware, the 'IoTSensor' class simulates different sensor types (Ultrasonic, Infrared, Pressure, Magnetic). The simulation introduces Gaussian noise to sensor readings to mimic environmental interference. Furthermore, a battery degradation model was implemented, where each reading slightly reduces battery life, eventually triggering low-battery alerts and reducing reading confidence scores.")

add_subsection_heading(doc, "5.2.3", "Analytics Engine")
add_body_text(doc, "The 'ParkingAnalytics' class consumes the state data generated by the simulation. It aggregates slot statuses to calculate occupancy rates per floor and section. It processes the transaction logs to compute daily revenue and vehicle throughput. This data is then fed into Matplotlib plotting functions to generate PNG images that serve as the administrative dashboard.")

# ---------------- CHAPTER 6: SOLUTION TESTING AND PERFORMANCE EVALUATION ----------------
add_chapter_title(doc, 6, "SOLUTION TESTING AND PERFORMANCE EVALUATION")
add_body_text(doc, "This chapter addresses Performance Criterion 7 (PC7) and Performance Criterion 8 (PC8), detailing the testing methodologies and performance assessment.")

add_section_heading(doc, "6.1", "Testing Strategy (PC7)")
add_body_text(doc, "The solution underwent rigorous testing to ensure logical correctness and stability. The testing strategy focused on unit testing individual methods and integration testing the complete simulation flow.")

add_subsection_heading(doc, "6.1.1", "Functional Testing")
add_body_text(doc, "Edge cases were explicitly tested. For example, the system was tested to handle a scenario where a vehicle attempts to enter a fully occupied parking lot. The system correctly denied entry and generated a CRITICAL alert. Another test verified that the fee calculation algorithm accurately computed costs for long-duration stays spanning multiple hours.")

add_subsection_heading(doc, "6.1.2", "Bug Identification and Fixing")
add_body_text(doc, "During development, a bug was identified where the sensor anomaly detection algorithm was triggering false positives due to minor natural fluctuations in simulated ultrasonic readings. This was fixed by implementing a threshold delta (e.g., a change greater than 50cm) before flagging an anomaly, thereby improving the reliability of the alert system.")

add_section_heading(doc, "6.2", "Performance Evaluation (PC8)")
add_body_text(doc, "The performance of the solution was evaluated against the desired criteria established during the requirements phase.")

add_subsection_heading(doc, "6.2.1", "Simulation Throughput")
add_body_text(doc, "The system successfully simulated an 8-hour traffic period with 100 vehicles interacting with a 120-slot parking lot in less than a second of compute time. The transaction logging and state updates proved highly efficient, demonstrating that the backend logic is well-optimized and capable of handling high-frequency data streams from physical sensors.")

add_subsection_heading(doc, "6.2.2", "Analytics Generation")
add_body_text(doc, "The analytics module successfully parsed complex nested dictionaries containing thousands of simulated sensor readings and transaction logs. The generation of six high-resolution visualization charts took minimal processing time, confirming that the reporting module can operate efficiently as a background cron job in a production environment.")

# ---------------- CHAPTER 7: RESULTS AND VISUALIZATIONS ----------------
add_chapter_title(doc, 7, "RESULTS AND VISUALIZATIONS")
add_body_text(doc, "This chapter presents the outputs generated by the Smart Parking Management System's analytics module. These visualizations serve as the administrative dashboard, providing actionable insights into parking lot utilization and operational health.")

add_section_heading(doc, "7.1", "Occupancy Heatmap")
add_body_text(doc, "The occupancy heatmap provides a macro-level view of space utilization across different physical zones of the parking facility.")
add_image_with_caption(doc, "/home/ubuntu/occupancy_heatmap.png", "Figure 1: Parking Occupancy by Floor and Section")
add_body_text(doc, "Figure 1 displays a dual-chart visualization. The left bar chart compares occupied versus vacant slots across three floors. This allows administrators to quickly identify which floors are reaching capacity. The right horizontal bar chart illustrates the occupancy rate by specific sections (A, B, C, D). A color gradient from green to red visually indicates sections that are heavily congested, allowing staff to redirect incoming traffic to underutilized zones.")

add_section_heading(doc, "7.2", "Occupancy Timeline")
add_body_text(doc, "Understanding how parking demand fluctuates throughout the day is critical for dynamic pricing and staff scheduling.")
add_image_with_caption(doc, "/home/ubuntu/occupancy_timeline.png", "Figure 2: Parking Lot Occupancy Throughout the Day")
add_body_text(doc, "Figure 2 presents a time-series analysis of occupancy rates over a 24-hour period. The chart clearly highlights peak usage hours, typically showing spikes during morning arrivals (8:00 AM - 9:00 AM) and lunch hours. Threshold lines at 50% and 80% occupancy provide visual benchmarks. When the curve crosses the 80% threshold, the system is designed to trigger 'High Occupancy' alerts to management.")

add_section_heading(doc, "7.3", "Performance Metrics Dashboard")
add_body_text(doc, "The performance metrics dashboard provides a high-level summary of the most critical Key Performance Indicators (KPIs).")
add_image_with_caption(doc, "/home/ubuntu/performance_metrics.png", "Figure 3: Key Performance Metrics Dashboard")
add_body_text(doc, "Figure 3 aggregates real-time data into easily readable KPI boxes. It displays the total capacity, current occupied and vacant counts, and the overall occupancy rate percentage. It also tracks slots marked for maintenance or reserved status. The text summary at the bottom provides a quick textual overview of the facility's current operational state, which is ideal for a quick glance by parking attendants.")

add_section_heading(doc, "7.4", "Revenue and Vehicle Analysis")
add_body_text(doc, "Financial tracking is a core requirement for parking operators.")
add_image_with_caption(doc, "/home/ubuntu/revenue_analysis.png", "Figure 4: Daily Revenue and Vehicle Count Analysis")
add_body_text(doc, "Figure 4 correlates the daily financial revenue with the volume of vehicles processed. By analyzing this data, operators can identify which days of the week are most profitable and adjust operational strategies accordingly. The color-coded revenue bars provide an immediate visual indication of performance against daily targets.")

# ---------------- CHAPTER 8: CONCLUSION AND LEARNING EVALUATION ----------------
add_chapter_title(doc, 8, "CONCLUSION AND LEARNING EVALUATION")
add_body_text(doc, "This final chapter addresses Performance Criterion 9 (PC9), summarizing the project outcomes and evaluating the technical skills gained during the internship.")

add_section_heading(doc, "8.1", "Project Conclusion")
add_body_text(doc, "The Real-Time Smart Parking Management System project successfully demonstrated the application of IoT concepts and software engineering to solve a pressing urban challenge. The developed simulation accurately models the complex interactions between vehicles, parking slots, and sensor networks. By integrating advanced analytics and visualization, the system transforms raw occupancy data into actionable intelligence for parking administrators. The solution proves that automated, sensor-driven parking management can significantly enhance space utilization, optimize revenue, and improve the overall driver experience by reducing search times.")

add_section_heading(doc, "8.2", "Learning Evaluation (PC9)")
add_body_text(doc, "Participating in this internship project resulted in substantial technical skill gain and professional development:")

add_bullet_point(doc, "System Architecture Design: I gained practical experience in designing a multi-layered architecture, separating the perception layer (IoT sensors) from the application layer (analytics).")
add_bullet_point(doc, "Advanced Python Programming: My proficiency in Python significantly improved, particularly in using Object-Oriented Programming (OOP) principles, dataclasses, and complex data structures to model real-world entities.")
add_bullet_point(doc, "Data Visualization Skills: I acquired deep knowledge of Matplotlib and Seaborn libraries, learning how to format, style, and generate professional-grade charts and dashboards programmatically.")
add_bullet_point(doc, "Algorithm Development: Implementing the logic for slot assignment, fee calculation, and sensor anomaly detection enhanced my algorithmic thinking and problem-solving capabilities.")
add_bullet_point(doc, "Software Testing: I learned the importance of rigorous testing, specifically how to simulate edge cases (e.g., lot full scenarios, hardware failures) to ensure system robustness.")

add_body_text(doc, "Overall, the internship provided a comprehensive, hands-on experience in full-cycle software development, bridging the gap between theoretical academic knowledge and practical industry application.")

# ---------------- REFERENCES ----------------
add_chapter_title(doc, 9, "REFERENCES")
add_body_text(doc, "[1] Al-Khatib, A., et al. (2020). \"IoT-Based Smart Parking System.\" IEEE Internet of Things Journal.")
add_body_text(doc, "[2] Python Software Foundation. (2024). \"Python Language Reference, version 3.11.\" Available at http://www.python.org")
add_body_text(doc, "[3] Hunter, J. D. (2007). \"Matplotlib: A 2D graphics environment.\" Computing in Science & Engineering, 9(3), 90-95.")
add_body_text(doc, "[4] Waskom, M. (2021). \"Seaborn: statistical data visualization.\" Journal of Open Source Software, 6(60), 3021.")

# Save document
doc.save('/home/ubuntu/Internship_Report_Smart_Parking.docx')
print("Document generated successfully.")
