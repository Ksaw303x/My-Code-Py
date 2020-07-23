from queue import Queue, Empty
from time import sleep
from threading import Timer


class CommandoLoader(object):
    def __init__(self):
        self.__bot = None
        self.__error_callback_function = None
        self.thread = None
        self.error_queue_function = None

    def start_demon(self, bot, error_queue_function, callback):
        self.__bot = bot
        self.error_queue_function = error_queue_function
        self.__start_auto_runner(None, callback, 10)
        print('Auto Run Demon Started')

    def __start_auto_runner(self, action, callback, interval: int):
        """
        :param action: a function that have to be executed
        :param interval: a time in seconds

        Run the function every interval seconds
        """

        def func():
            while True:
                try:
                    # here will be the stuff to run
                    # action()
                    raise Exception('An error occurred here.')

                except Exception as exc:
                    print(exc)
                    self.error_queue_function.put(exc)
                    callback(exc)
                sleep(interval)

        try:
            self.thread = Timer(interval=interval, function=func)  # wait in minutes
            self.thread.start()

        except Exception as e:
            print(e)


def main():
    error_queue_function = Queue()

    def callback(exc):
        # single error handling
        print('Message in chat for exc: {}'.format(exc))
        return

        # multiple error handling, with queue
        try:
            print(error_queue_function.empty())
            exc = error_queue_function.get(block=False)
            print(error_queue_function.empty())
        except Empty:
            pass
        else:
            print('Message in chat for exc: {}'.format(exc))

    cl = CommandoLoader()
    # none is the bot command to send messages
    cl.start_demon(None, error_queue_function, callback)


if __name__ == '__main__':
    main()
