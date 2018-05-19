from datetime import datetime

def getDescription(word, description):
    return f'You asked me to remind you {word} {description}.'

def getDatetimeDescription(date_time):
    date_time_obj = datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')
    return datetime.strftime(date_time_obj,'on %d, %b %Y at %H:%M:%S')

def reminder_quick_replies():
    return [
                {
                    'content_type': 'text',
                    'title': '✅ Mark as complete',
                    'payload': 'complete_reminder'
                },
                {
                    'content_type': 'text',
                    'title': '⏰ Remind me later',
                    'payload': 'reschedule_reminder'
                }
            ]