import random
from datetime import datetime, timedelta

class NudgeSystem:
    def __init__(self):
        """Initialize the nudge system with templates and rules"""
        self.nudge_templates = self._initialize_nudge_templates()
        self.nudge_rules = self._initialize_nudge_rules()
        
    def _initialize_nudge_templates(self):
        """Initialize nudge message templates"""
        return {
            'reminder': [
                "Don't forget to continue your learning journey! You have pending assignments.",
                "Your learning streak is at risk! Log in to keep it going.",
                "You've been away for a while. Your classmates are missing you!",
                "Quick reminder: You have {activity} due soon.",
                "Your study group is active today. Join the discussion!"
            ],
            'assessment': [
                "Ready for a quick knowledge check? Take this 5-minute quiz!",
                "Test your understanding with a micro-assessment.",
                "How confident are you with {topic}? Take a quick self-assessment.",
                "Your progress suggests you're ready for the next challenge!",
                "Complete this short quiz to unlock the next module."
            ],
            'challenge': [
                "Challenge accepted? Compete with {peer} in today's coding challenge!",
                "New peer challenge available: Who can complete {task} faster?",
                "Your study buddy {peer} just completed a challenge. Your turn!",
                "Weekly challenge: Can you maintain a 7-day learning streak?",
                "Group challenge: Work together to solve this real-world problem."
            ],
            'mentor': [
                "Your mentor {mentor_name} has shared new insights for you.",
                "Schedule a quick check-in with your mentor this week.",
                "Your mentor noticed you're struggling with {topic}. Get help now!",
                "Mentorship opportunity: Join today's office hours.",
                "Your mentor has answered your question about {topic}."
            ]
        }
    
    def _initialize_nudge_rules(self):
        """Initialize rules for when to trigger nudges"""
        return {
            'reminder': {
                'triggers': [
                    {'condition': 'hours_inactive', 'threshold': 24, 'priority': 'medium'},
                    {'condition': 'hours_inactive', 'threshold': 48, 'priority': 'high'},
                    {'condition': 'engagement_drop', 'threshold': 20, 'priority': 'high'},
                    {'condition': 'streak_risk', 'threshold': 1, 'priority': 'medium'}
                ]
            },
            'assessment': {
                'triggers': [
                    {'condition': 'completion_rate_low', 'threshold': 0.5, 'priority': 'medium'},
                    {'condition': 'time_spent_high', 'threshold': 2.0, 'priority': 'low'},
                    {'condition': 'no_assessment', 'threshold': 72, 'priority': 'high'}
                ]
            },
            'challenge': {
                'triggers': [
                    {'condition': 'engagement_moderate', 'threshold': 70, 'priority': 'low'},
                    {'condition': 'peer_active', 'threshold': 1, 'priority': 'medium'},
                    {'condition': 'streak_high', 'threshold': 7, 'priority': 'low'}
                ]
            },
            'mentor': {
                'triggers': [
                    {'condition': 'dropout_risk_high', 'threshold': 0.7, 'priority': 'high'},
                    {'condition': 'struggle_detected', 'threshold': 1, 'priority': 'high'},
                    {'condition': 'mentor_available', 'threshold': 1, 'priority': 'medium'}
                ]
            }
        }
    
    def _check_triggers(self, user_data, nudge_type):
        """Check if any triggers are met for a specific nudge type"""
        triggers = self.nudge_rules[nudge_type]['triggers']
        triggered = []
        
        for trigger in triggers:
            condition = trigger['condition']
            threshold = trigger['threshold']
            priority = trigger['priority']
            
            if self._evaluate_condition(user_data, condition, threshold):
                triggered.append({
                    'condition': condition,
                    'priority': priority,
                    'reason': self._get_trigger_reason(condition, threshold, user_data)
                })
        
        return triggered
    
    def _evaluate_condition(self, user_data, condition, threshold):
        """Evaluate if a specific condition is met"""
        if condition == 'hours_inactive':
            if user_data['last_active'] == 'Today':
                return False
            elif user_data['last_active'] == 'Yesterday':
                return threshold <= 24
            else:
                # Extract days from "X days ago"
                days = int(user_data['last_active'].split()[0]) if user_data['last_active'].split()[0].isdigit() else 1
                return (days * 24) >= threshold
                
        elif condition == 'engagement_drop':
            return user_data['engagement_score'] < (100 - threshold)
            
        elif condition == 'streak_risk':
            return user_data['streak'] <= threshold
            
        elif condition == 'completion_rate_low':
            return (user_data['completion_rate'] / 100) < threshold
            
        elif condition == 'time_spent_high':
            return user_data['avg_session'] > threshold
            
        elif condition == 'no_assessment':
            # Simulate time since last assessment
            return random.random() < 0.3  # 30% chance
            
        elif condition == 'engagement_moderate':
            return user_data['engagement_score'] > threshold
            
        elif condition == 'peer_active':
            return random.random() < 0.4  # 40% chance of peer activity
            
        elif condition == 'streak_high':
            return user_data['streak'] >= threshold
            
        elif condition == 'dropout_risk_high':
            return user_data['dropout_risk'] > threshold
            
        elif condition == 'struggle_detected':
            return user_data['completion_rate'] < 40  # Low completion suggests struggle
            
        elif condition == 'mentor_available':
            return random.random() < 0.6  # 60% chance mentor is available
        
        return False
    
    def _get_trigger_reason(self, condition, threshold, user_data):
        """Get human-readable reason for trigger"""
        reasons = {
            'hours_inactive': f"User inactive for {user_data['last_active']}",
            'engagement_drop': f"Engagement score dropped to {user_data['engagement_score']:.1f}%",
            'streak_risk': f"Learning streak at risk ({user_data['streak']} days)",
            'completion_rate_low': f"Low completion rate ({user_data['completion_rate']:.1f}%)",
            'time_spent_high': f"High session time ({user_data['avg_session']:.1f}h) may indicate difficulty",
            'no_assessment': "No recent assessment activity detected",
            'engagement_moderate': "Good engagement level - opportunity for challenge",
            'peer_active': "Peer activity detected - social learning opportunity",
            'streak_high': f"Strong learning streak ({user_data['streak']} days) - reward opportunity",
            'dropout_risk_high': f"High dropout risk ({user_data['dropout_risk']*100:.1f}%)",
            'struggle_detected': "Learning difficulties detected",
            'mentor_available': "Mentor support available"
        }
        
        return reasons.get(condition, f"Condition {condition} triggered")
    
    def _generate_nudge_message(self, nudge_type, user_data, trigger_info):
        """Generate a personalized nudge message"""
        templates = self.nudge_templates[nudge_type]
        base_message = random.choice(templates)
        
        # Personalize the message
        replacements = {
            '{activity}': random.choice(['Python Assignment', 'Data Analysis Quiz', 'Project Milestone']),
            '{topic}': random.choice(['Machine Learning', 'Data Structures', 'Web Development']),
            '{peer}': random.choice(['Alex', 'Maya', 'Jordan']),
            '{task}': random.choice(['Algorithm Challenge', 'Code Review', 'Project Setup']),
            '{mentor_name}': random.choice(['Dr. Smith', 'Prof. Johnson', 'Dr. Brown'])
        }
        
        for placeholder, replacement in replacements.items():
            base_message = base_message.replace(placeholder, replacement)
        
        return base_message
    
    def get_active_nudges(self, users_data):
        """Get currently active nudges for all users"""
        active_nudges = []
        
        for user in users_data:
            user_nudges = self.generate_nudges_for_user(user)
            # Limit to top 2 nudges per user for active display
            active_nudges.extend(user_nudges[:2])
        
        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        active_nudges.sort(key=lambda x: priority_order[x['priority']], reverse=True)
        
        return active_nudges
    
    def get_all_nudges(self, users_data):
        """Get all possible nudges for all users"""
        all_nudges = []
        
        for user in users_data:
            user_nudges = self.generate_nudges_for_user(user)
            all_nudges.extend(user_nudges)
        
        return all_nudges
    
    def generate_nudges_for_user(self, user_data):
        """Generate all applicable nudges for a specific user"""
        user_nudges = []
        
        for nudge_type in self.nudge_templates.keys():
            triggers = self._check_triggers(user_data, nudge_type)
            
            for trigger in triggers:
                message = self._generate_nudge_message(nudge_type, user_data, trigger)
                
                nudge = {
                    'user': user_data['name'],
                    'user_id': user_data['id'],
                    'type': nudge_type,
                    'message': message,
                    'priority': trigger['priority'],
                    'trigger_reason': trigger['reason'],
                    'created_at': datetime.now(),
                    'status': 'pending'
                }
                
                user_nudges.append(nudge)
        
        # Sort by priority within user nudges
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        user_nudges.sort(key=lambda x: priority_order[x['priority']], reverse=True)
        
        return user_nudges
    
    def send_nudge(self, nudge):
        """Simulate sending a nudge to a user"""
        # In a real system, this would integrate with email, SMS, push notifications, etc.
        return {
            'success': True,
            'method': random.choice(['email', 'push_notification', 'in_app']),
            'sent_at': datetime.now(),
            'nudge_id': f"nudge_{random.randint(1000, 9999)}"
        }
    
    def track_nudge_effectiveness(self, nudge, user_response):
        """Track the effectiveness of sent nudges"""
        # In a real system, this would track user responses and adjust nudge strategies
        effectiveness_metrics = {
            'nudge_id': nudge.get('nudge_id', 'unknown'),
            'response_time': random.uniform(0.5, 24.0),  # Hours to respond
            'response_type': user_response,  # 'engaged', 'dismissed', 'no_response'
            'engagement_change': random.uniform(-5, 15),  # Change in engagement score
            'recorded_at': datetime.now()
        }
        
        return effectiveness_metrics
    
    def get_urgent_nudges(self, user_data):
        """Get only urgent/critical nudges that require immediate attention"""
        urgent_nudges = []
        
        # Critical conditions that trigger urgent notifications
        urgent_conditions = []
        
        # Check for missed classes/low attendance
        if user_data.get('attendance_rate', 1.0) < 0.6:
            urgent_conditions.append({
                'type': 'attendance',
                'message': f"Your attendance is only {user_data.get('attendance_rate', 0)*100:.0f}%. Missing more classes puts you at risk of failing!",
                'priority': 'high',
                'reason': 'Low attendance detected'
            })
        
        # Check for very low engagement
        if user_data.get('engagement_score', 100) < 30:
            urgent_conditions.append({
                'type': 'engagement',
                'message': f"Your engagement has dropped to {user_data.get('engagement_score', 0):.0f}%. Immediate action needed to avoid dropout!",
                'priority': 'high', 
                'reason': 'Critical engagement drop'
            })
        
        # Check for high dropout risk
        if user_data.get('dropout_risk', 0) > 0.8:
            urgent_conditions.append({
                'type': 'dropout_risk',
                'message': "You're at high risk of dropping out. Please contact your mentor or advisor immediately!",
                'priority': 'high',
                'reason': 'Extremely high dropout risk detected'
            })
        
        # Check for failed evaluations (with zero division protection)
        evaluations_attempted = user_data.get('evaluations_attempted', 0)
        evaluations_passed = user_data.get('evaluations_passed', 0)
        if evaluations_attempted > 0 and (evaluations_passed / evaluations_attempted) < 0.4:
            urgent_conditions.append({
                'type': 'evaluations', 
                'message': f"You've only passed {evaluations_passed}/{evaluations_attempted} evaluations. Get help before it's too late!",
                'priority': 'high',
                'reason': 'Multiple evaluation failures'
            })
        
        # Check for very low grades
        avg_grade = (user_data.get('first_sem_grade', 10) + user_data.get('second_sem_grade', 10)) / 2
        if avg_grade < 8:  # Less than 8/20
            urgent_conditions.append({
                'type': 'grades',
                'message': f"Your average grade is {avg_grade:.1f}/20. Schedule tutoring sessions now!",
                'priority': 'high',
                'reason': 'Very low academic performance'
            })
        
        # Convert conditions to nudge format
        for condition in urgent_conditions:
            urgent_nudge = {
                'user': user_data['name'],
                'user_id': user_data['id'],
                'type': condition['type'],
                'message': condition['message'],
                'priority': condition['priority'],
                'trigger_reason': condition['reason'],
                'created_at': datetime.now(),
                'status': 'urgent',
                'is_urgent': True
            }
            urgent_nudges.append(urgent_nudge)
        
        return urgent_nudges
