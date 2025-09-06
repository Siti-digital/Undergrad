import bcrypt
import psycopg2
import os
import random
from typing import Optional, Dict, Any
import streamlit as st

class AuthManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.database_url)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, email: str, password: str, name: Optional[str] = None) -> bool:
        """Create a new user"""
        try:
            hashed_password = self.hash_password(password)
            if not name:
                name = email.split('@')[0].title()  # Use email prefix as name
            
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (email, password_hash, name) VALUES (%s, %s, %s) RETURNING id",
                        (email, hashed_password, name)
                    )
                    result = cursor.fetchone()
                    if result:
                        user_id = result[0]
                        # Create sample stats for new user
                        self._create_sample_stats(cursor, user_id)
                    conn.commit()
            return True
        except psycopg2.IntegrityError:
            # User already exists
            return False
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, email, password_hash, name FROM users WHERE email = %s",
                        (email,)
                    )
                    user_row = cursor.fetchone()
                    
                    if user_row and self.verify_password(password, user_row[2]):
                        # Get user stats
                        stats = self.get_user_stats(user_row[0])
                        user_data = {
                            'id': user_row[0],
                            'email': user_row[1],
                            'name': user_row[3],
                            'is_logged_in': True,
                            # Default values for compatibility
                            'engagement_score': 75.0,
                            'daily_time': 2.5,
                            'streak': 5,
                            'dropout_risk': 0.3,
                            'course_completion_rate': 70.0,
                            'total_study_hours': 45.0,
                            'assignments_completed': 8,
                            'assignments_total': 12,
                            'completion_rate': 0.70,
                            'total_time': 45.0,
                            'age_at_enrollment': 22,
                            'course_load': 4,
                            'attendance_rate': 0.45,  # Low attendance to trigger alerts
                            'first_sem_grade': 14.0,
                            'second_sem_grade': 14.0,
                            'evaluations_attempted': 10,
                            'evaluations_passed': 8,
                            'avg_session': 2.5,
                            'learning_style': 'visual',
                            'preferred_time': 'morning'
                        }
                        if stats:
                            user_data.update(stats)
                            # Update name from stats if available
                            user_data['name'] = user_row[3]
                        return user_data
            return None
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user data by email"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, email, name FROM users WHERE email = %s",
                        (email,)
                    )
                    user_row = cursor.fetchone()
                    
                    if user_row:
                        return {
                            'id': user_row[0],
                            'email': user_row[1],
                            'name': user_row[2]
                        }
            return None
        except Exception as e:
            st.error(f"Error fetching user: {str(e)}")
            return None
    
    def _create_sample_stats(self, cursor, user_id: int):
        """Create sample engagement stats for new user"""
        # Generate realistic sample stats based on different engagement levels
        engagement_level = random.choice(['high', 'moderate', 'at_risk'])
        
        if engagement_level == 'high':
            stats = {
                'engagement_score': round(random.uniform(75, 95), 2),
                'daily_time': round(random.uniform(3.0, 5.5), 2),
                'streak': random.randint(10, 25),
                'dropout_risk': round(random.uniform(0.1, 0.3), 3),
                'course_completion_rate': round(random.uniform(80, 95), 2),
                'total_study_hours': round(random.uniform(60, 120), 2),
                'assignments_completed': random.randint(9, 12),
                'assignments_total': 12
            }
        elif engagement_level == 'moderate':
            stats = {
                'engagement_score': round(random.uniform(25, 35), 2),  # Low engagement to trigger alerts
                'daily_time': round(random.uniform(2.0, 3.5), 2),
                'streak': random.randint(5, 15),
                'dropout_risk': round(random.uniform(0.7, 0.9), 3),  # High risk to trigger alerts
                'course_completion_rate': round(random.uniform(60, 80), 2),
                'total_study_hours': round(random.uniform(35, 65), 2),
                'assignments_completed': random.randint(6, 9),
                'assignments_total': 12
            }
        else:  # at_risk
            stats = {
                'engagement_score': round(random.uniform(15, 25), 2),  # Very low to trigger alerts
                'daily_time': round(random.uniform(0.5, 2.5), 2),
                'streak': random.randint(1, 8),
                'dropout_risk': round(random.uniform(0.8, 0.95), 3),  # Very high risk
                'course_completion_rate': round(random.uniform(20, 60), 2),
                'total_study_hours': round(random.uniform(10, 40), 2),
                'assignments_completed': random.randint(2, 6),
                'assignments_total': 12
            }
        
        cursor.execute("""
            INSERT INTO user_stats (
                user_id, engagement_score, daily_time, streak, dropout_risk,
                course_completion_rate, total_study_hours, assignments_completed, assignments_total
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, stats['engagement_score'], stats['daily_time'], stats['streak'],
            stats['dropout_risk'], stats['course_completion_rate'], stats['total_study_hours'],
            stats['assignments_completed'], stats['assignments_total']
        ))
    
    def get_user_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user engagement stats from database"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT engagement_score, daily_time, streak, dropout_risk,
                               course_completion_rate, total_study_hours, 
                               assignments_completed, assignments_total
                        FROM user_stats WHERE user_id = %s
                    """, (user_id,))
                    stats_row = cursor.fetchone()
                    
                    if stats_row:
                        return {
                            'engagement_score': float(stats_row[0]),
                            'daily_time': float(stats_row[1]),
                            'streak': int(stats_row[2]),
                            'dropout_risk': float(stats_row[3]),
                            'course_completion_rate': float(stats_row[4]),
                            'total_study_hours': float(stats_row[5]),
                            'assignments_completed': int(stats_row[6]),
                            'assignments_total': int(stats_row[7]),
                            # Add compatibility fields for existing code
                            'completion_rate': float(stats_row[4]) / 100.0,  # Convert % to decimal
                            'total_time': float(stats_row[5]),
                            'name': None  # Will be filled from user data
                        }
            return None
        except Exception as e:
            st.error(f"Database error occurred. Please try again.")
            return None