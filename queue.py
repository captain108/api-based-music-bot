from collections import defaultdict

queues = defaultdict(list)

def add_song(chat_id, song):
    queues[chat_id].append(song)

def next_song(chat_id):
    if queues[chat_id]:
        return queues[chat_id].pop(0)
    return None

def get_queue(chat_id):
    return queues[chat_id]

def clear_queue(chat_id):
    queues[chat_id].clear()
