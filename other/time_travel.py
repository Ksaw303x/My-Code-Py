from datetime import datetime, timedelta


class TimeTravel:
    def __init__(self):
        self.now = datetime.now()

    def fuck_go_back_by(self, hours=0, minutes=0):
        return self.now - timedelta(hours=hours, minutes=minutes)


if __name__ == '__main__':
    tt = TimeTravel()
    time = tt.fuck_go_back_by(hours=1, minutes=10)
    print(time)

