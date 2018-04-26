def quick_reply_features():
    return [
                {
                    'content_type': 'text',
                    'title': '🌤 Weather',
                    'payload': 'weather_request'
                },
                {
                    'content_type': 'text',
                    'title': '📰 News',
                    'payload': 'news_request'
                },
                {
                    'content_type': 'text',
                    'title': '📧 E-mail',
                    'payload': 'email_request'
                },
                {
                    'content_type': 'text',
                    'title': '⏰ Reminder',
                    'payload': 'reminder_request'
                },
                {
                    'content_type': 'text',
                    'title': '🗓 Calendar',
                    'payload': 'calendar_request'
                },
            ]
