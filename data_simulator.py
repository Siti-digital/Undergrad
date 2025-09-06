import random
import numpy as np
from datetime import datetime, timedelta

class DataSimulator:
    def __init__(self):
        """Initialize the data simulator with single user profile for personalized dashboard"""
        self.users = self._create_user_profiles()
        self.base_metrics = self._initialize_base_metrics()
        
    def _create_user_profiles(self):
        """Create single user profile for logged-in user based on dropout patterns"""
        # Simulate different user states - can be modified based on actual login
        import random
        
        # Generate a realistic user profile based on dataset patterns
        engagement_level = random.choice(['high', 'moderate', 'at_risk'])
        
        if engagement_level == 'high':
            profile = {
                'id': 1,
                'name': 'Current User',  # Will be replaced with actual user name
                'profile_type': 'high_engagement',
                'base_engagement': random.uniform(75, 95),
                'learning_style': random.choice(['visual', 'kinesthetic', 'auditory']),
                'preferred_time': random.choice(['morning', 'afternoon', 'evening']),
                'streak_tendency': random.uniform(0.8, 0.95),
                'age_at_enrollment': random.randint(18, 25),
                'course_load': random.randint(4, 6),
                'attendance_rate': random.uniform(0.85, 0.98)
            }
        elif engagement_level == 'moderate':
            profile = {
                'id': 1,
                'name': 'Current User',
                'profile_type': 'moderate_engagement', 
                'base_engagement': random.uniform(55, 75),
                'learning_style': random.choice(['visual', 'kinesthetic', 'auditory']),
                'preferred_time': random.choice(['morning', 'afternoon', 'evening']),
                'streak_tendency': random.uniform(0.6, 0.8),
                'age_at_enrollment': random.randint(20, 28),
                'course_load': random.randint(3, 5),
                'attendance_rate': random.uniform(0.70, 0.85)
            }
        else:  # at_risk
            profile = {
                'id': 1,
                'name': 'Current User',
                'profile_type': 'at_risk',
                'base_engagement': random.uniform(25, 55),
                'learning_style': random.choice(['visual', 'kinesthetic', 'auditory']),
                'preferred_time': random.choice(['morning', 'afternoon', 'evening']),
                'streak_tendency': random.uniform(0.3, 0.6),
                'age_at_enrollment': random.randint(22, 35),
                'course_load': random.randint(2, 4),
                'attendance_rate': random.uniform(0.45, 0.70)
            }
        
        return [profile]
    
    def _initialize_base_metrics(self):
        """Initialize base metrics for the current user based on dropout patterns"""
        user = self.users[0]  # Single user
        profile_type = user['profile_type']
        
        # Generate realistic metrics based on profile type and dataset patterns
        if profile_type == 'high_engagement':
            metrics = {
                'total_time': random.uniform(60, 120),
                'completion_rate': random.uniform(0.80, 0.95),
                'last_login': datetime.now() - timedelta(hours=random.randint(1, 12)),
                'session_count': random.randint(35, 80),
                'interaction_score': random.uniform(0.75, 0.95),
                'first_sem_grade': random.uniform(14, 20),  # Based on dataset scale
                'second_sem_grade': random.uniform(14, 20),
                'evaluations_attempted': random.randint(8, 12),
                'evaluations_passed': random.randint(7, 12)
            }
        elif profile_type == 'moderate_engagement':
            metrics = {
                'total_time': random.uniform(30, 80),
                'completion_rate': random.uniform(0.60, 0.80),
                'last_login': datetime.now() - timedelta(hours=random.randint(6, 36)),
                'session_count': random.randint(20, 45),
                'interaction_score': random.uniform(0.50, 0.75),
                'first_sem_grade': random.uniform(10, 16),
                'second_sem_grade': random.uniform(10, 16),
                'evaluations_attempted': random.randint(5, 10),
                'evaluations_passed': random.randint(4, 8)
            }
        else:  # at_risk
            metrics = {
                'total_time': random.uniform(10, 40),
                'completion_rate': random.uniform(0.20, 0.60),
                'last_login': datetime.now() - timedelta(hours=random.randint(24, 120)),
                'session_count': random.randint(5, 25),
                'interaction_score': random.uniform(0.15, 0.50),
                'first_sem_grade': random.uniform(0, 12),
                'second_sem_grade': random.uniform(0, 10),
                'evaluations_attempted': random.randint(2, 8),
                'evaluations_passed': random.randint(0, 4)
            }
        
        return {user['id']: metrics}
    
    def _calculate_engagement_score(self, user, current_metrics):
        """Calculate dynamic engagement score based on multiple factors"""
        base = user['base_engagement']
        
        # Time-based fluctuation
        time_factor = 1 + 0.1 * np.sin(datetime.now().hour * np.pi / 12)
        
        # Recent activity factor
        hours_since_login = (datetime.now() - current_metrics['last_login']).total_seconds() / 3600
        recency_factor = max(0.5, 1 - hours_since_login / 72)  # Decay over 3 days
        
        # Completion rate influence
        completion_factor = 0.8 + 0.4 * current_metrics['completion_rate']
        
        # Random daily variation
        daily_variation = random.uniform(0.9, 1.1)
        
        final_score = base * time_factor * recency_factor * completion_factor * daily_variation
        return max(0, min(100, final_score))
    
    def _calculate_dropout_risk(self, user, engagement_score, current_metrics):
        """Calculate dropout risk based on multiple indicators"""
        risk_factors = []
        
        # Low engagement risk
        if engagement_score < 40:
            risk_factors.append(0.4)
        elif engagement_score < 60:
            risk_factors.append(0.2)
        else:
            risk_factors.append(0.05)
        
        # Inactivity risk
        hours_since_login = (datetime.now() - current_metrics['last_login']).total_seconds() / 3600
        if hours_since_login > 48:
            risk_factors.append(0.3)
        elif hours_since_login > 24:
            risk_factors.append(0.15)
        else:
            risk_factors.append(0.05)
        
        # Low completion rate risk
        if current_metrics['completion_rate'] < 0.3:
            risk_factors.append(0.35)
        elif current_metrics['completion_rate'] < 0.6:
            risk_factors.append(0.15)
        else:
            risk_factors.append(0.05)
        
        # Low interaction risk
        if current_metrics['interaction_score'] < 0.3:
            risk_factors.append(0.2)
        elif current_metrics['interaction_score'] < 0.6:
            risk_factors.append(0.1)
        else:
            risk_factors.append(0.02)
        
        total_risk = min(0.95, sum(risk_factors))
        return total_risk
    
    def update_real_time_data(self):
        """Update metrics to simulate real-time changes"""
        for user_id, metrics in self.base_metrics.items():
            # Simulate some users being more active
            if random.random() < 0.3:  # 30% chance of activity update
                metrics['last_login'] = datetime.now() - timedelta(minutes=random.randint(1, 60))
                metrics['session_count'] += random.randint(0, 2)
                metrics['total_time'] += random.uniform(0, 2)
                metrics['interaction_score'] = min(1.0, metrics['interaction_score'] + random.uniform(-0.1, 0.2))
    
    def get_current_user_data(self):
        """Get comprehensive data for the current logged-in user"""
        user = self.users[0]  # Single user
        metrics = self.base_metrics[user['id']]
        engagement_score = self._calculate_engagement_score(user, metrics)
        dropout_risk = self._calculate_dropout_risk(user, engagement_score, metrics)
        
        # Calculate additional metrics
        avg_session = metrics['total_time'] / max(1, metrics['session_count'])
        daily_time = random.uniform(0.5, 4.0)
        streak = max(1, int(random.uniform(1, 30) * user['streak_tendency']))
        
        # Determine last active status
        hours_since_login = (datetime.now() - metrics['last_login']).total_seconds() / 3600
        if hours_since_login < 24:
            last_active = "Today"
        elif hours_since_login < 48:
            last_active = "Yesterday"
        else:
            last_active = f"{int(hours_since_login/24)} days ago"
        
        user_data = {
            'id': user['id'],
            'name': user['name'],
            'profile_type': user['profile_type'],
            'engagement_score': engagement_score,
            'dropout_risk': dropout_risk,
            'total_time': metrics['total_time'],
            'completion_rate': metrics['completion_rate'] * 100,
            'last_login': metrics['last_login'],
            'last_active': last_active,
            'session_count': metrics['session_count'],
            'avg_session': avg_session,
            'daily_time': daily_time,
            'streak': streak,
            'interaction_score': metrics['interaction_score'],
            'learning_style': user['learning_style'],
            'preferred_time': user['preferred_time'],
            'age_at_enrollment': user['age_at_enrollment'],
            'course_load': user['course_load'],
            'attendance_rate': user['attendance_rate'],
            'first_sem_grade': metrics['first_sem_grade'],
            'second_sem_grade': metrics['second_sem_grade'],
            'evaluations_attempted': metrics['evaluations_attempted'],
            'evaluations_passed': metrics['evaluations_passed']
        }
        
        return user_data
    
    def get_all_users_data(self):
        """Get data for all users (single user in this case) - for compatibility"""
        return [self.get_current_user_data()]
    
    def get_user_by_id(self, user_id):
        """Get specific user data by ID"""
        all_users = self.get_all_users_data()
        return next((user for user in all_users if user['id'] == user_id), None)
    
    def get_historical_data(self, user_id, days=30):
        """Generate historical data for trends and analysis"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        historical_data = []
        base_engagement = user['engagement_score']
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            
            # Add trend and noise
            trend = -0.5 + (i / days) * 1  # Slight upward trend
            noise = random.uniform(-5, 5)
            engagement = max(0, min(100, base_engagement + trend + noise))
            
            daily_data = {
                'date': date,
                'engagement_score': engagement,
                'time_spent': random.uniform(0.5, 4.0),
                'interactions': random.randint(5, 50),
                'completed_activities': random.randint(0, 5)
            }
            
            historical_data.append(daily_data)
        
        return historical_data
    
    def get_user_courses(self):
        """Get enrolled courses for the current user"""
        # Simulate realistic course enrollment
        courses = [
            {
                'id': 'CS101',
                'name': 'Introduction to Computer Science',
                'instructor': 'Dr. Sarah Johnson',
                'credits': 3,
                'status': 'Active',
                'progress': random.uniform(45, 85),
                'engagement_rate': random.uniform(60, 95),
                'current_grade': f"{random.uniform(75, 95):.1f}%",
                'next_assignment': f"Due in {random.randint(2, 14)} days"
            },
            {
                'id': 'MATH201',
                'name': 'Calculus II',
                'instructor': 'Prof. Michael Chen',
                'credits': 4,
                'status': 'Active',
                'progress': random.uniform(35, 75),
                'engagement_rate': random.uniform(45, 80),
                'current_grade': f"{random.uniform(70, 90):.1f}%",
                'next_assignment': f"Due in {random.randint(1, 7)} days"
            },
            {
                'id': 'ENG102',
                'name': 'Academic Writing',
                'instructor': 'Dr. Emily Rodriguez',
                'credits': 3,
                'status': 'Active',
                'progress': random.uniform(55, 90),
                'engagement_rate': random.uniform(70, 95),
                'current_grade': f"{random.uniform(80, 95):.1f}%",
                'next_assignment': f"Due in {random.randint(3, 10)} days"
            },
            {
                'id': 'PHYS101',
                'name': 'Physics Fundamentals',
                'instructor': 'Dr. Robert Kim',
                'credits': 4,
                'status': 'At Risk',
                'progress': random.uniform(25, 55),
                'engagement_rate': random.uniform(30, 65),
                'current_grade': f"{random.uniform(60, 75):.1f}%",
                'next_assignment': f"Due in {random.randint(1, 3)} days"
            }
        ]
        
        # Adjust courses based on user's dropout risk
        user_data = self.get_current_user_data()
        if user_data['dropout_risk'] > 0.6:
            # Make more courses at risk
            for course in courses[-2:]:
                course['engagement_rate'] = random.uniform(25, 55)
                course['status'] = 'At Risk'
        
        return courses
