from ast import Constant
from multiprocessing.connection import wait
import random

from locust import HttpUser, between, task

wait_time = between(10, 600)


class test_load(HttpUser):

    @task
    def test_main(self):
        self.wait()
        # assume all users arrive at the index page
        self.client.get("")
    
    @task
    def test_play(self):
        self.wait()
        self.client.get("play/" + str(random.randint(1,162)))
        wait_time = between(8000,15000)
        self.wait()