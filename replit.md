# UnderGrad - Learner Engagement Dashboard

## Overview

UnderGrad is a comprehensive learner engagement analytics platform designed to track, analyze, and improve student learning outcomes through data-driven insights and intelligent nudging systems. The application provides real-time monitoring of student engagement patterns, risk assessment for at-risk learners, and automated interventions to maintain learning momentum.

The platform focuses on three core functionalities: engagement analytics that identify learning patterns and risks, a sophisticated nudging system that provides personalized interventions, and comprehensive dashboards that visualize student progress and institutional metrics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses Streamlit as the primary frontend framework, providing an interactive web-based dashboard with real-time data visualization. The architecture follows a single-page application pattern with multiple views accessible through sidebar navigation. Key components include:

- **Dashboard View**: Real-time engagement metrics and overview statistics
- **Analytics View**: Deep-dive analysis with advanced visualizations using Plotly
- **Nudge Center**: Management interface for intervention strategies
- **Classes/Courses Views**: Detailed academic content tracking

The frontend implements automatic refresh mechanisms (30-second intervals) to ensure real-time data updates and maintains session state for consistent user experience across navigation.

### Backend Architecture
The system employs a modular Python architecture with three core components:

- **DataSimulator**: Generates realistic user engagement data with diverse learner profiles (high engagement, moderate engagement, at-risk)
- **EngagementAnalytics**: Processes engagement data to calculate risk scores, trends, and behavioral patterns
- **NudgeSystem**: Implements intelligent intervention logic with rule-based triggering and personalized messaging

Each component operates independently but shares data through the main application controller, enabling loose coupling and easy extensibility.

### Data Management
The application currently uses in-memory data simulation for demonstration purposes, with structured user profiles containing:

- Engagement metrics (completion rates, time spent, interaction frequency)
- Learning preferences (visual, kinesthetic, auditory learning styles)
- Behavioral patterns (preferred study times, streak tendencies)
- Risk assessment scores and historical trends

The data layer is designed to be easily replaceable with actual database connections for production deployment.

### Analytics Engine
The engagement analytics system implements multiple calculation methods:

- **Risk Stratification**: Categorizes learners into low, medium, and high-risk groups based on engagement thresholds
- **Trend Analysis**: Tracks engagement patterns over time to predict future behavior
- **Interaction Pattern Recognition**: Identifies optimal learning times and preferred content types
- **Prediction Modeling**: Calculates accuracy metrics for intervention effectiveness

### Nudging System Architecture
The intelligent nudging system operates on a rule-based engine with:

- **Template-Based Messaging**: Categorized nudge templates (reminders, assessments, challenges, mentorship)
- **Trigger Rules**: Conditional logic based on inactivity periods, engagement drops, and behavioral patterns
- **Personalization Layer**: Dynamic content insertion based on individual learner profiles
- **Priority Scheduling**: Multi-level priority system for intervention timing

## External Dependencies

### Visualization Libraries
- **Plotly Express & Graph Objects**: Interactive charting and data visualization
- **Plotly Subplots**: Complex multi-panel dashboard layouts

### Data Processing
- **Pandas**: Data manipulation and analysis for engagement metrics
- **NumPy**: Numerical computations for statistical analysis and trend calculations

### Web Framework
- **Streamlit**: Primary web application framework providing the user interface and real-time capabilities

### Python Standard Libraries
- **datetime/timedelta**: Time-based calculations for engagement tracking and nudge timing
- **random**: Data simulation and variation generation for realistic user behavior patterns
- **time**: Session management and auto-refresh functionality

The application is designed to be framework-agnostic for future database integration, with current simulation components easily replaceable with actual data sources such as learning management systems, student information systems, or educational analytics platforms.