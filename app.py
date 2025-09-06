import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import random
import os

from data_simulator import DataSimulator
from nudge_system import NudgeSystem
from auth_manager import AuthManager

# Page configuration
st.set_page_config(
    page_title="UnderGrad - Learner Engagement Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication manager
if 'auth_manager' not in st.session_state:
    st.session_state.auth_manager = AuthManager()

# Initialize user session
if 'user' not in st.session_state:
    st.session_state.user = None

# Authentication Check
if not st.session_state.user or not st.session_state.user.get('is_logged_in', False):
    # Show login/signup page
    st.markdown("""
    <div style="
        text-align: center;
        padding: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin: 20px;
        color: white;
    ">
        <h1 style="font-size: 3em; margin-bottom: 20px;">🎓 Welcome to UnderGrad</h1>
        <p style="font-size: 1.3em; margin-bottom: 30px;">Your Personal Learning Dashboard</p>
        <p style="font-size: 1.1em; opacity: 0.9; margin-bottom: 40px;">Track your engagement, predict risks, and stay on top of your academic goals</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Login/Signup form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Initialize form state
        if 'show_signup' not in st.session_state:
            st.session_state.show_signup = False
        
        if st.session_state.show_signup:
            # Sign Up Form
            st.markdown("""
            <div style="
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                text-align: center;
            ">
                <h2 style="color: #333; margin-bottom: 30px;">Create Your Account</h2>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("signup_form"):
                email = st.text_input("Email Address", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                name = st.text_input("Full Name (optional)", placeholder="Enter your full name")
                
                signup_button = st.form_submit_button("Sign Up", use_container_width=True, type="primary")
                
                if signup_button:
                    if not email or not password:
                        st.error("Please fill in all required fields.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        # Create user
                        if st.session_state.auth_manager.create_user(email, password, name):
                            st.success("Account created successfully! Please sign in.")
                            st.session_state.show_signup = False
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("Email already exists. Please sign in instead.")
            
            if st.button("Already have an account? Sign In", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
        
        else:
            # Sign In Form
            st.markdown("""
            <div style="
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                text-align: center;
            ">
                <h2 style="color: #333; margin-bottom: 30px;">Sign In</h2>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("signin_form"):
                email = st.text_input("Email Address", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                signin_button = st.form_submit_button("Sign In", use_container_width=True, type="primary")
                
                if signin_button:
                    if not email or not password:
                        st.error("Please enter both email and password.")
                    else:
                        # Authenticate user
                        user = st.session_state.auth_manager.authenticate_user(email, password)
                        if user:
                            st.session_state.user = user
                            st.success(f"Welcome back, {user['name']}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Invalid email or password. Please try again or sign up.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Don't have an account? Sign Up", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()
    
    st.stop()  # Stop execution here if not logged in

# Initialize session state
if 'data_simulator' not in st.session_state:
    st.session_state.data_simulator = DataSimulator()
    st.session_state.nudge_system = NudgeSystem()
    st.session_state.last_update = datetime.now()
    st.session_state.current_page = 'Dashboard'

# Auto-refresh every 30 seconds
if datetime.now() - st.session_state.last_update > timedelta(seconds=30):
    st.session_state.data_simulator.update_real_time_data()
    st.session_state.last_update = datetime.now()
    st.rerun()

# Sidebar Navigation
with st.sidebar:
    st.title("🎓 UnderGrad")
    st.markdown("---")
    
    # Navigation menu
    page = st.selectbox(
        "Navigate to:",
        ["Dashboard", "Analytics", "Classes"],
        index=["Dashboard", "Analytics", "Classes"].index(st.session_state.current_page) if st.session_state.current_page in ["Dashboard", "Analytics", "Classes"] else 0
    )
    
    # Update session state based on selectbox
    if page != st.session_state.current_page:
        st.session_state.current_page = page
        st.rerun()
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("Quick Actions")
    
    if st.button("📚 My Courses", use_container_width=True):
        st.session_state.current_page = "My Courses"
        st.rerun()
    
    if st.button("👥 Find Study Groups", use_container_width=True):
        st.success("Connecting to study groups...")
    
    if st.button("💬 Contact Mentor", use_container_width=True):
        st.success("Mentor chat initiated...")
    
    st.markdown("---")
    
    # User Stats Summary  
    st.subheader("📊 Your Quick Stats")
    # Get stats from authenticated user instead of simulator
    if st.session_state.user:
        user_stats = st.session_state.user
        st.metric("📈 Engagement", f"{user_stats.get('engagement_score', 75):.1f}%")
        st.metric("⏰ Today", f"{user_stats.get('daily_time', 2.5):.1f}h")
        st.metric("🔥 Streak", f"{user_stats.get('streak', 5)} days")
        
        # Quick risk indicator
        dropout_risk = user_stats.get('dropout_risk', 0.3)
        if dropout_risk > 0.7:
            st.error("⚠️ High Risk")
        elif dropout_risk > 0.4:
            st.warning("⚡ At Risk")
        else:
            st.success("✅ On Track")
    else:
        # Fallback if no user data
        st.metric("📈 Engagement", "N/A")
        st.metric("⏰ Today", "N/A")
        st.metric("🔥 Streak", "N/A")
    
    st.markdown("---")
    
    # Display logged-in user info and logout button
    if st.session_state.user and st.session_state.user.get('is_logged_in', False):
        st.markdown(f"""
        <div style="
            background: #E8F5E8;
            border: 1px solid #4CAF50;
            border-radius: 8px;
            padding: 10px;
            margin: 10px 0;
            text-align: center;
        ">
            <p style="margin: 0; color: #2E7D32; font-weight: bold;">👤 {st.session_state.user.get('name', 'User')}</p>
            <p style="margin: 5px 0 0 0; color: #2E7D32; font-size: 0.9em;">{st.session_state.user.get('email', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.show_signup = False
            st.rerun()

# Use session state for page navigation
page = st.session_state.current_page

# Notification Bell System (appears on all pages)
def show_notification_bell():
    # Use authenticated user data instead of simulator
    user_data = st.session_state.user if st.session_state.user else {}
    urgent_nudges = st.session_state.nudge_system.get_urgent_nudges(user_data)
    
    if urgent_nudges:
        # Initialize popup state
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = False
        
        # Create a container for notification bell in the top right
        st.markdown(f"""
        <div id="notification-container" style="
            position: fixed;
            top: 60px;
            right: 20px;
            z-index: 999;
        ">
            <div onclick="window.showNotificationPopup()" style="
                background: #FF6B6B;
                color: white;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                animation: pulse 2s infinite;
                user-select: none;
            ">
                🔔 {len(urgent_nudges)}
            </div>
        </div>
        
        <style>
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
        </style>
        
        <script>
            window.showNotificationPopup = function() {{
                const popup = document.getElementById('urgentNotificationPopup');
                if (popup) {{
                    popup.style.display = popup.style.display === 'none' ? 'flex' : 'none';
                }}
            }}
        </script>
        """, unsafe_allow_html=True)
        
        # Simple notification popup using expander
        with st.expander(f"🔔 {len(urgent_nudges)} Urgent Alerts - Click to View", expanded=False):
            st.markdown("### ⚠️ Urgent Course Alerts")
            
            # Display urgent nudges
            for nudge in urgent_nudges[:3]:
                alert_type = nudge['type'].title().replace('_', ' ')
                if nudge['type'] == 'attendance':
                    st.error(f"**📚 {alert_type}**: {nudge['message']}")
                elif nudge['type'] == 'engagement':
                    st.warning(f"**📊 {alert_type}**: {nudge['message']}")
                elif nudge['type'] == 'dropout_risk':
                    st.error(f"**⚠️ {alert_type}**: {nudge['message']}")
                elif nudge['type'] == 'evaluations':
                    st.warning(f"**📝 {alert_type}**: {nudge['message']}")
                elif nudge['type'] == 'grades':
                    st.error(f"**📊 {alert_type}**: {nudge['message']}")
                else:
                    st.info(f"**{alert_type}**: {nudge['message']}")
            
            if st.button("📞 Get Academic Support", type="primary", use_container_width=True):
                st.success("Connecting you with academic support...")
        
        # Position the expander in the top right (CSS styling)
        st.markdown("""
        <style>
            /* Style the expander to look like a notification popup */
            .streamlit-expanderHeader {
                background-color: #FF6B6B !important;
                color: white !important;
                border-radius: 10px !important;
                font-weight: bold !important;
            }
            
            .streamlit-expanderContent {
                background-color: white !important;
                border: 2px solid #FF6B6B !important;
                border-radius: 10px !important;
                margin-top: 5px !important;
            }
        </style>
        """, unsafe_allow_html=True)

# Main Dashboard
if page == "Dashboard":
    # Show notification bell
    show_notification_bell()
    # Get current user data
    user_data = st.session_state.user if st.session_state.user else {}
    
    # Personalized Welcome Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        color: white;
        text-align: center;
    ">
        <h1 style="margin: 0; font-size: 2.5em;">👋 Welcome Back, {st.session_state.user.get('name', 'Student')}!</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">Your Personal Learning Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Personal Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📈 Your Engagement Score", 
            f"{user_data['engagement_score']:.1f}%",
            delta=f"{random.uniform(-2, 3):.1f}%",
            help="Your overall learning engagement level"
        )
    
    with col2:
        risk_level = "Low" if user_data['dropout_risk'] < 0.3 else "Medium" if user_data['dropout_risk'] < 0.7 else "High"
        st.metric(
            "🎯 Dropout Risk", 
            risk_level,
            delta=f"{user_data['dropout_risk']*100:.1f}%",
            help="Your current risk level of dropping out"
        )
    
    with col3:
        st.metric(
            "⏰ Total Learning Time", 
            f"{user_data['total_time']:.1f}h",
            delta=f"+{random.uniform(1, 5):.1f}h",
            help="Your total time spent learning"
        )
    
    with col4:
        st.metric(
            "🔥 Current Streak", 
            f"{user_data['streak']} days",
            delta=1 if random.random() > 0.5 else 0,
            help="Your daily learning streak"
        )
    
    st.markdown("---")
    
    # Main Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Your Learning Journey")
        
        # Create personal engagement trend chart
        dates = pd.date_range(end=datetime.now(), periods=14, freq='D')
        engagement_trend = [
            max(0, min(100, user_data['engagement_score'] + random.uniform(-15, 15)))
            for _ in range(14)
        ]
        
        fig_engagement = go.Figure()
        fig_engagement.add_trace(go.Scatter(
            x=dates,
            y=engagement_trend,
            mode='lines+markers',
            name='Your Engagement',
            line=dict(width=4, color='#667eea'),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig_engagement.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Engagement Score (%)",
            hovermode='x',
            showlegend=False
        )
        
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Your Performance Metrics")
        
        # Personal performance radar chart
        categories = ['Engagement', 'Completion Rate', 'Attendance', 'Grade Average', 'Time Spent']
        values = [
            user_data['engagement_score'],
            user_data['completion_rate'], 
            user_data['attendance_rate'] * 100,
            (user_data['first_sem_grade'] + user_data['second_sem_grade']) * 2.5,  # Scale to 0-100
            min(100, (user_data['total_time'] / 100) * 100)  # Scale to 0-100
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Your Performance',
            line=dict(color='#764ba2', width=3),
            fillcolor='rgba(118, 75, 162, 0.2)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Personal Analytics Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏱️ Your Time Distribution")
        
        # Personal time spent by category
        time_categories = ['Videos', 'Assignments', 'Discussions', 'Quizzes']
        time_values = [random.uniform(0.5, 4.0) for _ in time_categories]
        
        fig_time = px.pie(
            values=time_values,
            names=time_categories,
            title="How You Spend Your Learning Time",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        )
        
        fig_time.update_layout(height=400)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        st.subheader("📊 Your Weekly Activity")
        
        # Personal weekly activity pattern
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        activity_hours = [random.uniform(0.5, 4.0) for _ in days]
        
        fig_activity = px.bar(
            x=days,
            y=activity_hours,
            title="Your Daily Learning Hours This Week",
            color=activity_hours,
            color_continuous_scale='Viridis'
        )
        
        fig_activity.update_layout(
            height=400,
            xaxis_title="Day of Week",
            yaxis_title="Hours Studied",
            showlegend=False
        )
        
        st.plotly_chart(fig_activity, use_container_width=True)
    
    # Personal Recommendations Section (removed from dashboard per user request)

elif page == "Analytics":
    # Show notification bell
    show_notification_bell()
    
    st.title("📊 Your Advanced Analytics")
    st.markdown("Deep dive into your learning patterns and progress")
    
    user_data = st.session_state.user if st.session_state.user else {}
    
    # Personal analytics overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 Engagement Score", f"{user_data['engagement_score']:.1f}%")
        st.metric("✅ Completion Rate", f"{user_data['completion_rate']:.1f}%")
        st.metric("👤 Age at Enrollment", f"{user_data['age_at_enrollment']} years")
    
    with col2:
        st.metric("⏰ Total Learning Time", f"{user_data['total_time']:.1f}h")
        st.metric("📚 Average Session", f"{user_data['avg_session']:.1f}h")
        st.metric("📋 Course Load", f"{user_data['course_load']} courses")
    
    with col3:
        st.metric("⚠️ Dropout Risk", f"{user_data['dropout_risk']*100:.1f}%")
        st.metric("🔥 Current Streak", f"{user_data['streak']} days")
        st.metric("🎯 Attendance Rate", f"{user_data['attendance_rate']*100:.0f}%")
    
    st.markdown("---")
    
    # Academic Performance Section
    st.subheader("🎓 Your Academic Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Semester grades comparison
        semesters = ['1st Semester', '2nd Semester']
        grades = [user_data['first_sem_grade'], user_data['second_sem_grade']]
        
        fig_grades = px.bar(
            x=semesters,
            y=grades,
            title="Your Grade Performance by Semester",
            color=grades,
            color_continuous_scale='RdYlGn',
            labels={'y': 'Grade (0-20 scale)', 'x': 'Semester'}
        )
        fig_grades.update_layout(height=400)
        st.plotly_chart(fig_grades, use_container_width=True)
    
    with col2:
        # Evaluation success rate
        evaluation_data = {
            'Status': ['Passed', 'Failed'],
            'Count': [user_data['evaluations_passed'], 
                     user_data['evaluations_attempted'] - user_data['evaluations_passed']]
        }
        
        fig_evals = px.pie(
            values=evaluation_data['Count'],
            names=evaluation_data['Status'],
            title="Your Evaluation Success Rate",
            color_discrete_sequence=['#4CAF50', '#F44336']
        )
        fig_evals.update_layout(height=400)
        st.plotly_chart(fig_evals, use_container_width=True)
    
    # Learning Pattern Analysis
    st.subheader("⏰ Your Learning Pattern Analysis")
    
    # Generate personalized hourly activity pattern based on preferred time
    hours = list(range(24))
    preferred_time = user_data['preferred_time']
    
    if preferred_time == 'morning':
        peak_hour = 9
    elif preferred_time == 'afternoon': 
        peak_hour = 14
    else:  # evening
        peak_hour = 19
    
    activity = [
        max(0, np.random.normal(
            loc=10 if abs(hour - peak_hour) < 3 else 2,
            scale=3
        )) for hour in hours
    ]
    
    fig_pattern = px.line(
        x=hours,
        y=activity,
        title=f"Your Daily Activity Pattern (Peak: {preferred_time.title()})",
        labels={'x': 'Hour of Day', 'y': 'Activity Level'}
    )
    fig_pattern.update_traces(line_color='#667eea', line_width=3)
    fig_pattern.update_layout(height=400)
    
    st.plotly_chart(fig_pattern, use_container_width=True)
    
    # Personal insights based on data
    st.subheader("💡 Your Personalized Insights")
    
    # Generate insights based on user data
    insights = []
    
    if user_data['dropout_risk'] > 0.7:
        insights.append("⚠️ **High Risk Alert**: Your engagement patterns suggest you may be at risk of dropping out. Consider reaching out to your mentor for support.")
    elif user_data['dropout_risk'] > 0.4:
        insights.append("⚡ **Moderate Risk**: Your performance shows some concerning patterns. Focus on improving attendance and completion rates.")
    else:
        insights.append("✅ **Low Risk**: Great job! Your engagement levels suggest you're on track to successfully complete your courses.")
    
    if user_data['streak'] > 10:
        insights.append(f"🔥 **Streak Master**: Amazing! You've maintained a {user_data['streak']}-day learning streak. Keep up the excellent consistency!")
    
    if user_data['completion_rate'] < 60:
        insights.append("📚 **Focus on Completion**: Your completion rate could use improvement. Try breaking tasks into smaller, manageable chunks.")
    
    if user_data['attendance_rate'] < 0.75:
        insights.append("🎯 **Attendance Focus**: Regular attendance strongly correlates with success. Try to maintain consistent participation.")
    
    for insight in insights:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea22, #FFFFFF);
            border-left: 4px solid #667eea;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        ">
            {insight}
        </div>
        """, unsafe_allow_html=True)

elif page == "My Courses":
    # Show notification bell
    show_notification_bell()
    
    st.title("📚 My Courses")
    st.markdown("Track your enrolled courses and engagement levels")
    
    user_data = st.session_state.user if st.session_state.user else {}
    courses = st.session_state.data_simulator.get_user_courses()
    
    if courses:
        # Course overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Total Courses", len(courses))
        
        with col2:
            avg_progress = np.mean([course['progress'] for course in courses])
            st.metric("📈 Avg Progress", f"{avg_progress:.1f}%")
        
        with col3:
            active_courses = len([c for c in courses if c['status'] == 'Active'])
            st.metric("✅ Active Courses", active_courses)
        
        with col4:
            at_risk_courses = len([c for c in courses if c['engagement_rate'] < 60])
            st.metric("⚠️ At Risk", at_risk_courses)
        
        st.markdown("---")
        
        # Display each course
        for course in courses:
            # Course card with engagement bar
            engagement_color = '#4CAF50' if course['engagement_rate'] >= 80 else '#FFA726' if course['engagement_rate'] >= 60 else '#FF6B6B'
            status_color = '#4CAF50' if course['status'] == 'Active' else '#9E9E9E' if course['status'] == 'Completed' else '#FF9800'
            
            st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                padding: 20px;
                margin: 15px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <div>
                        <h3 style="margin: 0 0 5px 0; color: #333;">{course['name']}</h3>
                        <p style="margin: 0; color: #666; font-size: 0.9em;">{course['instructor']} • {course['credits']} Credits</p>
                    </div>
                    <div style="
                        background: {status_color};
                        color: white;
                        padding: 4px 12px;
                        border-radius: 20px;
                        font-size: 0.8em;
                        font-weight: bold;
                    ">{course['status']}</div>
                </div>
                
                <div style="margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-size: 0.9em; font-weight: bold;">Engagement Rate</span>
                        <span style="font-size: 0.9em; color: {engagement_color}; font-weight: bold;">{course['engagement_rate']:.1f}%</span>
                    </div>
                    <div style="
                        background: #F0F0F0;
                        border-radius: 10px;
                        height: 8px;
                        overflow: hidden;
                    ">
                        <div style="
                            background: {engagement_color};
                            height: 100%;
                            width: {course['engagement_rate']}%;
                            border-radius: 10px;
                            transition: width 0.3s ease;
                        "></div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                    <div>
                        <span style="font-size: 0.8em; color: #666;">Progress: </span>
                        <span style="font-size: 0.8em; font-weight: bold;">{course['progress']:.1f}%</span>
                    </div>
                    <div>
                        <span style="font-size: 0.8em; color: #666;">Next Assignment: </span>
                        <span style="font-size: 0.8em; font-weight: bold;">{course['next_assignment']}</span>
                    </div>
                    <div>
                        <span style="font-size: 0.8em; color: #666;">Grade: </span>
                        <span style="font-size: 0.8em; font-weight: bold;">{course['current_grade']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick actions for each course
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button(f"📚 View Content", key=f"content_{course['id']}"):
                    st.success(f"Opening {course['name']} content...")
            with col2:
                if st.button(f"📅 Assignments", key=f"assignments_{course['id']}"):
                    st.info(f"Loading assignments for {course['name']}...")
            with col3:
                if st.button(f"📈 Progress", key=f"progress_{course['id']}"):
                    st.info(f"Viewing detailed progress for {course['name']}...")
            with col4:
                if st.button(f"💬 Discussion", key=f"discussion_{course['id']}"):
                    st.info(f"Opening {course['name']} discussion forum...")
            
            st.markdown("---")
    
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
        ">
            <h2>📚 No Courses Enrolled</h2>
            <p style="font-size: 1.2em; margin: 15px 0;">Start your learning journey by enrolling in courses!</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Classes":
    # Show notification bell
    show_notification_bell()
    
    st.title("🏫 Class Management")
    
    st.subheader("Available Classes")
    
    classes = [
        {"name": "Advanced Python Programming", "instructor": "Dr. Smith", "time": "Mon/Wed 2:00 PM", "enrolled": 24, "capacity": 30},
        {"name": "Data Science Fundamentals", "instructor": "Prof. Johnson", "time": "Tue/Thu 10:00 AM", "enrolled": 28, "capacity": 30},
        {"name": "Machine Learning Basics", "instructor": "Dr. Brown", "time": "Mon/Wed 4:00 PM", "enrolled": 15, "capacity": 25},
        {"name": "Web Development", "instructor": "Prof. Wilson", "time": "Fri 1:00 PM", "enrolled": 20, "capacity": 30}
    ]
    
    for class_info in classes:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.write(f"**{class_info['name']}**")
                st.write(f"Instructor: {class_info['instructor']}")
            
            with col2:
                st.write(f"Schedule: {class_info['time']}")
                st.write(f"Enrolled: {class_info['enrolled']}/{class_info['capacity']}")
            
            with col3:
                progress = class_info['enrolled'] / class_info['capacity']
                st.progress(progress)
            
            with col4:
                if st.button("Join", key=f"join_{class_info['name']}"):
                    st.success(f"Successfully enrolled in {class_info['name']}!")

elif page == "Courses":
    # Colorful header with vibrant styling
    st.markdown("""
    <h1 style="
        color: #FF1744; 
        text-align: center; 
        font-size: 3em; 
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    ">📚 Course Catalog</h1>
    <p style="
        color: #1976D2; 
        text-align: center; 
        font-size: 1.2em; 
        font-weight: bold;
        margin-top: 0;
    ">🌟 Discover Amazing Courses That Will Transform Your Career! 🌟</p>
    """, unsafe_allow_html=True)
    
    # Enhanced course data with vibrant color schemes
    courses = [
        {
            "name": "🐍 Complete Python Bootcamp",
            "instructor": "Dr. Sarah Mitchell",
            "price": "$99",
            "original_price": "$199",
            "rating": 4.8,
            "students": 1200,
            "duration": "12 weeks",
            "level": "Beginner to Advanced",
            "description": "Master Python programming from basics to advanced concepts with hands-on projects and real-world applications.",
            "highlights": ["40+ coding exercises", "3 portfolio projects", "Lifetime access", "Certificate of completion"],
            "category": "Programming",
            "color": "#2196F3"  # Blue
        },
        {
            "name": "📊 Data Analysis with Pandas",
            "instructor": "Prof. Michael Chen", 
            "price": "$79",
            "original_price": "$149",
            "rating": 4.7,
            "students": 800,
            "duration": "8 weeks",
            "level": "Intermediate",
            "description": "Learn to analyze and manipulate data using Python's powerful Pandas library with real datasets.",
            "highlights": ["Real dataset analysis", "Data visualization", "Statistical insights", "Industry case studies"],
            "category": "Data Science",
            "color": "#4CAF50"  # Green
        },
        {
            "name": "🤖 Machine Learning A-Z",
            "instructor": "Dr. Emily Rodriguez",
            "price": "$149", 
            "original_price": "$249",
            "rating": 4.9,
            "students": 2000,
            "duration": "16 weeks",
            "level": "Advanced",
            "description": "Comprehensive machine learning course covering supervised and unsupervised learning with practical implementations.",
            "highlights": ["15+ algorithms", "Python & R", "Real ML projects", "Job interview prep"],
            "category": "Machine Learning",
            "color": "#9C27B0"  # Purple/Violet
        },
        {
            "name": "🌐 Web Development Masterclass",
            "instructor": "Prof. James Wilson",
            "price": "$119",
            "original_price": "$199", 
            "rating": 4.6,
            "students": 1500,
            "duration": "14 weeks",
            "level": "Beginner to Intermediate",
            "description": "Build modern web applications using HTML, CSS, JavaScript, React, and Node.js with professional deployment.",
            "highlights": ["5 full-stack projects", "Modern frameworks", "Responsive design", "Cloud deployment"],
            "category": "Web Development",
            "color": "#FF5722"  # Red-Orange
        },
        {
            "name": "📈 Data Visualization with Plotly",
            "instructor": "Dr. Anna Thompson",
            "price": "$69",
            "original_price": "$129",
            "rating": 4.5,
            "students": 650,
            "duration": "6 weeks", 
            "level": "Intermediate",
            "description": "Create stunning interactive visualizations and dashboards using Plotly and Dash frameworks.",
            "highlights": ["Interactive dashboards", "Business analytics", "Custom visualizations", "Publication-ready charts"],
            "category": "Data Visualization",
            "color": "#FF9800"  # Orange
        },
        {
            "name": "⚖️ AI Ethics & Responsible AI",
            "instructor": "Prof. David Kumar",
            "price": "$89",
            "original_price": "$159",
            "rating": 4.4,
            "students": 400,
            "duration": "10 weeks",
            "level": "All Levels", 
            "description": "Explore the ethical implications of AI technology and learn to develop responsible AI systems.",
            "highlights": ["Bias detection", "Fairness metrics", "Regulatory compliance", "Case study analysis"],
            "category": "AI Ethics",
            "color": "#607D8B"  # Blue Grey
        }
    ]
    
    # Create course displays using Streamlit components with vibrant colors
    for i, course in enumerate(courses):
        # Create colorful containers using Streamlit's native components
        with st.container():
            # Course Header with vibrant colors
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <h2 style="
                    color: {course['color']}; 
                    margin: 0; 
                    font-size: 1.8em;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
                ">{course['name']}</h2>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <p style="
                    color: #1A1A1A; 
                    font-size: 1.1em; 
                    font-weight: 500;
                    margin: 5px 0;
                ">👨‍🏫 <strong>{course['instructor']}</strong></p>
                """, unsafe_allow_html=True)
            
            with col2:
                # Bright pricing display
                st.markdown(f"""
                <div style="text-align: right;">
                    <span style="
                        color: #757575; 
                        text-decoration: line-through; 
                        font-size: 1em;
                    ">{course['original_price']}</span><br>
                    <span style="
                        color: #FF1744; 
                        font-size: 2em; 
                        font-weight: bold;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
                    ">{course['price']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Course details in colorful metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="⭐ Rating", 
                    value=f"{course['rating']}/5.0",
                    delta=f"{course['students']:,} students"
                )
            
            with col2:
                st.metric(
                    label="⏱️ Duration", 
                    value=course['duration'],
                    delta=course['level']
                )
                
            with col3:
                st.metric(
                    label="📚 Category",
                    value=course['category'],
                    delta="🎯 Popular"
                )
                
            with col4:
                # Enrollment button with bright colors
                if st.button(
                    f"🛒 ENROLL NOW!", 
                    key=f"enroll_{course['name']}", 
                    use_container_width=True,
                    type="primary"
                ):
                    st.success(f"🎉 Successfully enrolled in {course['name']}!")
                    st.balloons()
            
            # Course description with colorful styling
            st.markdown(f"""
            <p style="
                background: linear-gradient(90deg, {course['color']}22, #FFFFFF);
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid {course['color']};
                font-size: 1.1em;
                line-height: 1.6;
                margin: 15px 0;
            ">{course['description']}</p>
            """, unsafe_allow_html=True)
            
            # Course highlights with vibrant colors
            st.markdown(f"""
            <div style="
                background: {course['color']}11;
                border: 2px solid {course['color']};
                border-radius: 10px;
                padding: 15px;
                margin: 15px 0;
            ">
                <h4 style="color: {course['color']}; margin-top: 0;">✨ Course Highlights:</h4>
            """, unsafe_allow_html=True)
            
            # Display highlights in colorful columns
            highlight_cols = st.columns(2)
            for j, highlight in enumerate(course['highlights']):
                with highlight_cols[j % 2]:
                    st.markdown(f"""
                    <div style="
                        background: white;
                        padding: 8px;
                        border-radius: 5px;
                        border-left: 3px solid {course['color']};
                        margin: 5px 0;
                        font-weight: 500;
                    ">• {highlight}</div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add colorful separator
            st.markdown(f"""
            <hr style="
                border: none;
                height: 3px;
                background: linear-gradient(90deg, {course['color']}, transparent);
                margin: 30px 0;
            ">
            """, unsafe_allow_html=True)
    
    # Vibrant call-to-action section
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: #FFF9C4;
            color: #F57F17;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border: 2px solid #FDD835;
        ">
            <h3>⚡ Learning Streak</h3>
            <p>Keep your momentum going!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: #C8E6C9;
            color: #2E7D32;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border: 2px solid #4CAF50;
        ">
            <h3>✅ Goals on Track</h3>
            <p>You're doing great!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: #FFF9C4;
            color: #F57F17;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border: 2px solid #FDD835;
        ">
            <h3>📚 Study Time</h3>
            <p>Quality learning sessions</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>UnderGrad Learning Platform - Empowering Student Success Through Data-Driven Insights</p>
        <p>Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    unsafe_allow_html=True
)
