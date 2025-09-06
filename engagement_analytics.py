import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

class EngagementAnalytics:
    def __init__(self):
        """Initialize the engagement analytics engine"""
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
        
    def calculate_metrics(self, users_data):
        """Calculate comprehensive engagement metrics"""
        metrics = {
            'overall_engagement': self._calculate_overall_engagement(users_data),
            'risk_distribution': self._calculate_risk_distribution(users_data),
            'time_analytics': self._calculate_time_analytics(users_data),
            'interaction_patterns': self._calculate_interaction_patterns(users_data),
            'prediction_accuracy': self._calculate_prediction_accuracy(users_data)
        }
        return metrics
    
    def _calculate_overall_engagement(self, users_data):
        """Calculate overall engagement statistics"""
        engagement_scores = [user['engagement_score'] for user in users_data]
        
        return {
            'average': np.mean(engagement_scores),
            'median': np.median(engagement_scores),
            'std_dev': np.std(engagement_scores),
            'min': np.min(engagement_scores),
            'max': np.max(engagement_scores),
            'trend': self._calculate_engagement_trend(users_data)
        }
    
    def _calculate_engagement_trend(self, users_data):
        """Calculate engagement trend over time"""
        # Simulate trend calculation (in real app, this would use historical data)
        trends = []
        for user in users_data:
            if user['profile_type'] == 'high_engagement':
                trend = random.uniform(0.5, 2.0)  # Positive trend
            elif user['profile_type'] == 'moderate_engagement':
                trend = random.uniform(-0.5, 1.0)  # Mixed trend
            else:
                trend = random.uniform(-2.0, 0.5)  # Negative trend
            trends.append(trend)
        
        return np.mean(trends)
    
    def _calculate_risk_distribution(self, users_data):
        """Calculate distribution of dropout risk levels"""
        risk_counts = {'low': 0, 'medium': 0, 'high': 0}
        
        for user in users_data:
            risk = user['dropout_risk']
            if risk < self.risk_thresholds['low']:
                risk_counts['low'] += 1
            elif risk < self.risk_thresholds['medium']:
                risk_counts['medium'] += 1
            else:
                risk_counts['high'] += 1
        
        total_users = len(users_data)
        return {
            'counts': risk_counts,
            'percentages': {
                level: (count / total_users) * 100 
                for level, count in risk_counts.items()
            }
        }
    
    def _calculate_time_analytics(self, users_data):
        """Calculate time-based analytics"""
        total_times = [user['total_time'] for user in users_data]
        session_times = [user['avg_session'] for user in users_data]
        daily_times = [user['daily_time'] for user in users_data]
        
        return {
            'total_learning_time': {
                'sum': sum(total_times),
                'average': np.mean(total_times),
                'distribution': self._create_time_distribution(total_times)
            },
            'average_session_length': {
                'overall': np.mean(session_times),
                'by_user_type': self._session_time_by_type(users_data)
            },
            'daily_engagement': {
                'average': np.mean(daily_times),
                'peak_hours': self._identify_peak_hours(users_data)
            }
        }
    
    def _create_time_distribution(self, times):
        """Create time distribution buckets"""
        buckets = {'0-10h': 0, '10-30h': 0, '30-60h': 0, '60h+': 0}
        
        for time in times:
            if time < 10:
                buckets['0-10h'] += 1
            elif time < 30:
                buckets['10-30h'] += 1
            elif time < 60:
                buckets['30-60h'] += 1
            else:
                buckets['60h+'] += 1
        
        return buckets
    
    def _session_time_by_type(self, users_data):
        """Calculate average session time by user engagement type"""
        type_sessions = {}
        
        for user in users_data:
            user_type = user['profile_type']
            if user_type not in type_sessions:
                type_sessions[user_type] = []
            type_sessions[user_type].append(user['avg_session'])
        
        return {
            user_type: np.mean(sessions) 
            for user_type, sessions in type_sessions.items()
        }
    
    def _identify_peak_hours(self, users_data):
        """Identify peak learning hours based on user preferences"""
        time_preferences = [user['preferred_time'] for user in users_data]
        time_counts = {}
        
        for pref in time_preferences:
            time_counts[pref] = time_counts.get(pref, 0) + 1
        
        return sorted(time_counts.items(), key=lambda x: x[1], reverse=True)
    
    def _calculate_interaction_patterns(self, users_data):
        """Calculate user interaction patterns"""
        interaction_scores = [user['interaction_score'] for user in users_data]
        
        return {
            'average_interaction': np.mean(interaction_scores),
            'interaction_distribution': self._create_interaction_buckets(interaction_scores),
            'engagement_correlation': self._calculate_interaction_engagement_correlation(users_data)
        }
    
    def _create_interaction_buckets(self, scores):
        """Create interaction score buckets"""
        buckets = {'low': 0, 'medium': 0, 'high': 0}
        
        for score in scores:
            if score < 0.4:
                buckets['low'] += 1
            elif score < 0.7:
                buckets['medium'] += 1
            else:
                buckets['high'] += 1
        
        return buckets
    
    def _calculate_interaction_engagement_correlation(self, users_data):
        """Calculate correlation between interaction and engagement"""
        interactions = [user['interaction_score'] for user in users_data]
        engagements = [user['engagement_score'] for user in users_data]
        
        # Simple correlation calculation
        if len(interactions) > 1:
            return np.corrcoef(interactions, engagements)[0, 1]
        return 0
    
    def _calculate_prediction_accuracy(self, users_data):
        """Simulate prediction accuracy metrics"""
        # In a real system, this would compare predictions with actual outcomes
        base_accuracy = 0.85
        
        # Adjust based on data quality indicators
        data_quality = self._assess_data_quality(users_data)
        adjusted_accuracy = base_accuracy * data_quality
        
        return {
            'overall_accuracy': adjusted_accuracy,
            'precision': adjusted_accuracy * random.uniform(0.95, 1.05),
            'recall': adjusted_accuracy * random.uniform(0.9, 1.0),
            'f1_score': adjusted_accuracy * random.uniform(0.92, 1.02)
        }
    
    def _assess_data_quality(self, users_data):
        """Assess the quality of available data for predictions"""
        quality_factors = []
        
        # Check data completeness
        complete_records = len([u for u in users_data if u['session_count'] > 5])
        completeness = complete_records / len(users_data)
        quality_factors.append(completeness)
        
        # Check data recency
        recent_users = len([u for u in users_data if u['last_active'] in ['Today', 'Yesterday']])
        recency = recent_users / len(users_data)
        quality_factors.append(recency)
        
        # Check engagement variance (more variance = better for predictions)
        engagements = [u['engagement_score'] for u in users_data]
        variance_score = min(1.0, float(np.std(engagements)) / 30)  # Normalize to 0-1
        quality_factors.append(variance_score)
        
        return np.mean(quality_factors)
    
    def generate_insights(self, users_data):
        """Generate actionable insights from the analytics"""
        insights = []
        metrics = self.calculate_metrics(users_data)
        
        # Engagement insights
        avg_engagement = metrics['overall_engagement']['average']
        if avg_engagement < 50:
            insights.append({
                'type': 'warning',
                'title': 'Low Overall Engagement',
                'message': f'Average engagement is only {avg_engagement:.1f}%. Consider implementing engagement boosters.',
                'action': 'Review content difficulty and add interactive elements'
            })
        
        # Risk insights
        high_risk_pct = metrics['risk_distribution']['percentages']['high']
        if high_risk_pct > 30:
            insights.append({
                'type': 'alert',
                'title': 'High Dropout Risk',
                'message': f'{high_risk_pct:.1f}% of users are at high risk of dropping out.',
                'action': 'Activate intensive intervention protocols'
            })
        
        # Time insights
        avg_session = metrics['time_analytics']['average_session_length']['overall']
        if avg_session < 0.5:
            insights.append({
                'type': 'info',
                'title': 'Short Session Duration',
                'message': f'Average session length is {avg_session:.1f}h. Users may benefit from bite-sized content.',
                'action': 'Consider micro-learning modules'
            })
        
        return insights
