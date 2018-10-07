
class Usage(object):
    def __init__(self, time, user, room, available):
        self.time = time
        self.user = user
        self.room = room
        self.available = available


def get_usages(room, histories):

    usages = []
    for history in histories:
        # if the history type is not a changed field.
        if history.history_type != '~':
            continue

        delta = history.diff_against(history.prev_record)

        for change in delta.changes:
            if change.field == 'available':
                usages.append(Usage(time=history.history_date, user=history.history_user, room=history, available=change.new))

    return usages
