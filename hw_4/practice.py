import codecs
from multiprocessing import Pipe, Queue, Process, Manager
import sys
from time import sleep


class Logger:
    def __init__(self):
        self.queue = Manager().Queue()

    def log(self, msg):
        self.queue.put(msg)

    def save(self, path):
        with open(path, "w") as file:
            while not self.queue.empty():
                file.write(self.queue.get() + "\n")


class MainProcess(Process):
    def __init__(self, logger, recv_pipe, send_pipe):
        super(MainProcess, self).__init__()
        self.logger = logger
        self.recv_pipe = recv_pipe
        self.send_pipe = send_pipe

    def run(self):
        while True:
            msg = sys.stdin.readline()

            if msg.strip() == "Stop":
                self.send_pipe.send(msg.strip())
                break

            self.send_pipe.send(msg)
            self.logger.log(f"Sent from 'main' message '{msg.strip()}'")

            msg = self.recv_pipe.recv()
            self.logger.log(f"Received to 'main' message '{msg.strip()}'")
            sys.stdout.write(msg)


class A(Process):
    def __init__(self, recv_pipe, send_pipe):
        super(A, self).__init__()
        self.queue = Queue()
        self.recv_pipe = recv_pipe
        self.send_pipe = send_pipe
        self.stop_message = "Stop"

    def run(self):
        while True:
            while self.recv_pipe.poll(1):
                msg = self.recv_pipe.recv()
                self.queue.put(msg)

            if not self.queue.empty():
                msg = self.queue.get()
                self.send_pipe.send(msg.lower())
                if msg == self.stop_message:
                    break

            sleep(5)


class B(Process):
    def __init__(self, recv_pipe, send_pipe):
        super(B, self).__init__()
        self.recv_pipe = recv_pipe
        self.send_pipe = send_pipe
        self.stop_message = "Stop".lower()

    def run(self):
        while True:
            msg = None
            if self.recv_pipe.poll(1):
                msg = self.recv_pipe.recv()

                if msg == self.stop_message:
                    break

            if msg is not None:
                coded = codecs.encode(msg, "rot_13")
                self.send_pipe.send(coded)


def create_processes(logger):
    (recv_main, send_main) = Pipe()
    (recv_a, send_a) = Pipe()
    (recv_b, send_b) = Pipe()

    m = MainProcess(logger, recv_main, send_a)
    a = A(recv_a, send_b)
    b = B(recv_b, send_main)

    return m, a, b


def run_processes(ps):
    for p in ps:
        p.start()


def join_processes(ps):
    for p in ps:
        p.join()


def main():
    logger = Logger()
    m, a, b = create_processes(logger)
    run_processes([a, b])
    m.run()
    join_processes([a, b])
    logger.save("artifacts/practice_log.txt")


if __name__ == "__main__":
    main()
