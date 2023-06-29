from datetime import datetime

months = {
    1: 'січня',
    2: 'лютого',
    3: 'березня',
    4: 'квітня',
    5: 'травня',
    6: 'червня',
    7: 'липня',
    8: 'серпня',
    9: 'вересня',
    10: 'жовтня',
    11: 'листопада',
    12: 'грудня'
}


def date_or_time(date_obj):
    current_datetime = datetime.now()
    if current_datetime.date() == date_obj.date():
        return date_obj.strftime('%H:%M')
    elif current_datetime.year == date_obj.year:
        return f"{date_obj.day} {months[date_obj.month]} {date_obj.strftime('%H:%M')}"
    else:
        return date_obj.strftime('%Y-%m-%d')


def messages_to_json(messages):
    lst_msgs = []
    for message in messages:
        lst_msgs.append(message_to_json(message))
    return lst_msgs


def message_to_json(message):
    return {
        "from_user_id": message.from_user_id,
        "to_user_id": message.to_user_id,
        "content": message.content,
        "timestamp": date_or_time(message.timestamp),
        "read": message.read,
    }