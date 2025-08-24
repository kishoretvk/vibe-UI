from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# In-memory storage for notifications (in a real app, this would be a database)
notifications = {}
notification_id_counter = 1

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "notification-service",
        "version": "1.0.0"
    })

# Get all notifications
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    return jsonify(list(notifications.values()))

# Get specific notification
@app.route('/api/notifications/<notification_id>', methods=['GET'])
def get_notification(notification_id):
    notification_id = int(notification_id)
    if notification_id in notifications:
        return jsonify(notifications[notification_id])
    else:
        return jsonify({"error": "Notification not found"}), 404

# Create new notification
@app.route('/api/notifications', methods=['POST'])
def create_notification():
    global notification_id_counter
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['type', 'recipients', 'subject', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Create new notification
    new_notification = {
        "id": notification_id_counter,
        "type": data['type'],  # email, slack, teams, webhook
        "recipients": data['recipients'],  # list of recipients
        "subject": data['subject'],
        "message": data['message'],
        "status": "pending",  # pending, sent, failed
        "created_at": datetime.now().isoformat(),
        "sent_at": None
    }
    
    # Send notification based on type
    try:
        if data['type'] == 'email':
            send_email_notification(new_notification)
            new_notification['status'] = "sent"
            new_notification['sent_at'] = datetime.now().isoformat()
        elif data['type'] == 'slack':
            # Placeholder for Slack integration
            new_notification['status'] = "sent"
            new_notification['sent_at'] = datetime.now().isoformat()
        elif data['type'] == 'teams':
            # Placeholder for Teams integration
            new_notification['status'] = "sent"
            new_notification['sent_at'] = datetime.now().isoformat()
        elif data['type'] == 'webhook':
            # Placeholder for webhook integration
            new_notification['status'] = "sent"
            new_notification['sent_at'] = datetime.now().isoformat()
        else:
            new_notification['status'] = "failed"
            new_notification['error'] = "Unsupported notification type"
    except Exception as e:
        new_notification['status'] = "failed"
        new_notification['error'] = str(e)
    
    notifications[notification_id_counter] = new_notification
    notification_id_counter += 1
    
    return jsonify(new_notification), 201

# Update notification
@app.route('/api/notifications/<notification_id>', methods=['PUT'])
def update_notification(notification_id):
    notification_id = int(notification_id)
    
    if notification_id not in notifications:
        return jsonify({"error": "Notification not found"}), 404
    
    data = request.get_json()
    
    # Update notification
    notification = notifications[notification_id]
    
    # Updateable fields
    updatable_fields = ['type', 'recipients', 'subject', 'message', 'status']
    for field in updatable_fields:
        if field in data:
            notification[field] = data[field]
    
    notification['updated_at'] = datetime.now().isoformat()
    
    return jsonify(notification)

# Delete notification
@app.route('/api/notifications/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification_id = int(notification_id)
    
    if notification_id not in notifications:
        return jsonify({"error": "Notification not found"}), 404
    
    del notifications[notification_id]
    return jsonify({"message": "Notification deleted successfully"})

def send_email_notification(notification):
    """Send email notification"""
    # This is a simplified implementation
    # In a real app, you would use actual SMTP settings from environment variables
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    # If SMTP credentials are not configured, skip sending
    if not smtp_username or not smtp_password:
        print("SMTP credentials not configured, skipping email send")
        return
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ', '.join(notification['recipients'])
    msg['Subject'] = notification['subject']
    
    # Add body to email
    msg.attach(MIMEText(notification['message'], 'plain'))
    
    # Create SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable security
    server.login(smtp_username, smtp_password)
    
    # Send email
    text = msg.as_string()
    server.sendmail(smtp_username, notification['recipients'], text)
    server.quit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port, debug=True)