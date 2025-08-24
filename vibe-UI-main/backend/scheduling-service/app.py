from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# In-memory storage for scheduled reports (in a real app, this would be a database)
scheduled_reports = {}
scheduled_report_id_counter = 1

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "scheduling-service",
        "version": "1.0.0"
    })

# Get all scheduled reports
@app.route('/api/schedules', methods=['GET'])
def get_scheduled_reports():
    return jsonify(list(scheduled_reports.values()))

# Get specific scheduled report
@app.route('/api/schedules/<schedule_id>', methods=['GET'])
def get_scheduled_report(schedule_id):
    schedule_id = int(schedule_id)
    if schedule_id in scheduled_reports:
        return jsonify(scheduled_reports[schedule_id])
    else:
        return jsonify({"error": "Schedule not found"}), 404

# Create new scheduled report
@app.route('/api/schedules', methods=['POST'])
def create_scheduled_report():
    global scheduled_report_id_counter
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['report_template_id', 'schedule_frequency', 'destination']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Create new scheduled report
    new_schedule = {
        "id": scheduled_report_id_counter,
        "report_template_id": data['report_template_id'],
        "schedule_frequency": data['schedule_frequency'],  # daily, weekly, monthly
        "schedule_time": data.get('schedule_time', '09:00'),  # Time of day to run
        "destination": data['destination'],  # email, file system, etc.
        "recipients": data.get('recipients', []),  # Email addresses for notifications
        "parameters": data.get('parameters', {}),
        "enabled": data.get('enabled', True),
        "created_at": datetime.now().isoformat(),
        "last_run": None,
        "next_run": None
    }
    
    # Add to scheduler if enabled
    if new_schedule['enabled']:
        job_id = f"schedule_{scheduled_report_id_counter}"
        trigger = create_cron_trigger(new_schedule['schedule_frequency'], new_schedule['schedule_time'])
        scheduler.add_job(run_scheduled_report, trigger, id=job_id, args=[scheduled_report_id_counter])
        new_schedule['next_run'] = scheduler.get_job(job_id).next_run_time.isoformat()
    
    scheduled_reports[scheduled_report_id_counter] = new_schedule
    scheduled_report_id_counter += 1
    
    return jsonify(new_schedule), 201

# Update scheduled report
@app.route('/api/schedules/<schedule_id>', methods=['PUT'])
def update_scheduled_report(schedule_id):
    schedule_id = int(schedule_id)
    
    if schedule_id not in scheduled_reports:
        return jsonify({"error": "Schedule not found"}), 404
    
    data = request.get_json()
    
    # Update schedule
    schedule = scheduled_reports[schedule_id]
    
    # Updateable fields
    updatable_fields = ['report_template_id', 'schedule_frequency', 'schedule_time', 'destination', 'recipients', 'parameters', 'enabled']
    for field in updatable_fields:
        if field in data:
            schedule[field] = data[field]
    
    # Update scheduler job if needed
    job_id = f"schedule_{schedule_id}"
    existing_job = scheduler.get_job(job_id)
    
    # Remove existing job if it exists
    if existing_job:
        scheduler.remove_job(job_id)
    
    # Add new job if enabled
    if schedule['enabled']:
        trigger = create_cron_trigger(schedule['schedule_frequency'], schedule['schedule_time'])
        scheduler.add_job(run_scheduled_report, trigger, id=job_id, args=[schedule_id])
        schedule['next_run'] = scheduler.get_job(job_id).next_run_time.isoformat()
    else:
        schedule['next_run'] = None
    
    schedule['updated_at'] = datetime.now().isoformat()
    
    return jsonify(schedule)

# Delete scheduled report
@app.route('/api/schedules/<schedule_id>', methods=['DELETE'])
def delete_scheduled_report(schedule_id):
    schedule_id = int(schedule_id)
    
    if schedule_id not in scheduled_reports:
        return jsonify({"error": "Schedule not found"}), 404
    
    # Remove from scheduler
    job_id = f"schedule_{schedule_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    
    del scheduled_reports[schedule_id]
    return jsonify({"message": "Schedule deleted successfully"})

# Trigger a scheduled report immediately
@app.route('/api/schedules/<schedule_id>/trigger', methods=['POST'])
def trigger_scheduled_report(schedule_id):
    schedule_id = int(schedule_id)
    
    if schedule_id not in scheduled_reports:
        return jsonify({"error": "Schedule not found"}), 404
    
    # Run the report immediately
    run_scheduled_report(schedule_id)
    
    return jsonify({"message": "Scheduled report triggered", "schedule": scheduled_reports[schedule_id]})

def create_cron_trigger(frequency, schedule_time):
    """Create a cron trigger based on frequency and schedule time"""
    hour, minute = map(int, schedule_time.split(':'))
    
    if frequency == 'daily':
        return CronTrigger(hour=hour, minute=minute)
    elif frequency == 'weekly':
        return CronTrigger(day_of_week='mon', hour=hour, minute=minute)
    elif frequency == 'monthly':
        return CronTrigger(day=1, hour=hour, minute=minute)
    else:
        # Default to daily
        return CronTrigger(hour=hour, minute=minute)

def run_scheduled_report(schedule_id):
    """Run a scheduled report"""
    if schedule_id in scheduled_reports:
        schedule = scheduled_reports[schedule_id]
        print(f"Running scheduled report {schedule_id}: {schedule['report_template_id']}")
        
        # Update last run time
        schedule['last_run'] = datetime.now().isoformat()
        
        # Update next run time
        job_id = f"schedule_{schedule_id}"
        job = scheduler.get_job(job_id)
        if job:
            schedule['next_run'] = job.next_run_time.isoformat()
        
        # In a real implementation, this would trigger the actual report generation
        # and send it to the specified destination

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5007))
    app.run(host='0.0.0.0', port=port, debug=True)