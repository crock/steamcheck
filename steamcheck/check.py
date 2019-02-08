import os.path
import time
import csv
from collections import namedtuple
import random
import threading
from queue import Queue
import requests


class Checker(object):

    print_lock = threading.Lock()
    queue = Queue()
    thread_count = 1

    id_url = "https://steamcommunity.com/id/{}"
    group_url = "https://steamcommunity.com/groups/{}"

    output_list = ""
    word_list = ""
    proxy_list = ""

    words = []
    all_proxies = []
    good_proxies = []

    def __init__(self, args):
        self.output_list = args.output

        if args.word_list is not None:
            self.word_list = args.word_list
            self.get_words()

        if args.proxy_list is not None:
            self.proxy_list = args.proxy_list
            self.load_proxies_from_csv()

        if args.check_proxy is True:
            self.check_proxy_list()

        if int(args.thread_count) > 1:
            if int(args.thread_count) > 50:
                print("Max number of threads is limited to 50. Setting it for you.\nResuming in 2 seconds...")
                self.thread_count = 50
            else:
                self.thread_count = int(args.thread_count)

        try:
            self.check()
        except KeyboardInterrupt:
            print("\nExecution terminated by user.")
            exit(1)


    def get_words(self):
        if os.path.exists(self.word_list):
            with open(self.word_list, 'r') as fp:
                self.words = fp.readlines()
        else:
            raise Exception("Word list does not exist. Check your path and try again.")

    def load_proxies_from_csv(self):
        """
        A function which loads proxies from a .csv file, to a list.

        Inputs: path to .csv file which contains proxies, described by fields: 'ip', 'port', 'protocol'.

        Outputs: list containing proxies stored in named tuples.
        """
        Proxy = namedtuple('Proxy', ['ip', 'port', 'protocol'])

        if os.path.exists(self.proxy_list):
            with open(self.proxy_list, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                self.all_proxies = [Proxy(line['ip'], line['port'], line['protocol']) for line in csv_reader]
        else:
            raise Exception("Proxy list does not exist. Check your path and try again.")

    def check_proxy(self, proxy_ip, proxy_port, protocol):
        full_proxy = f'{protocol}://{proxy_ip}:{proxy_port}'
        proxies = {'http': full_proxy, 'https': full_proxy}
        try:
            r = requests.get('https://www.wikipedia.org', proxies=proxies, timeout=4)
            return_proxy = r.headers['X-Client-IP']
            if proxy_ip == return_proxy:
                print(f'{return_proxy} is good.')
                return True
            else:
                return False
        except Exception:
            return False

    def check_proxy_list(self):
        working_proxies = []

        for proxy in self.all_proxies:
            time.sleep(1)
            if self.check_proxy(proxy.ip, proxy.port, proxy.protocol):
                working_proxies.append(proxy)

        if len(working_proxies) > 0:
            print(f'Found {len(working_proxies)} working proxies.')
            self.good_proxies = working_proxies

        else:
            raise Exception("Found no working proxies.")

    def log_result(self, word, type, status):
        print(f'{word} ({type}) = {status}')

        with open(self.output_list, 'a') as fp:
            fp.write(f'{word} ({type})\n')

    def parse_job(self, item):
        word = self.words[item].strip('\n')
        proxy = None

        urls = [
            self.id_url.format(word),
            self.group_url.format(word)
        ]

        s = requests.Session()
        if self.proxy_list is not "":
            random_proxy = random.choice(self.good_proxies)
            proxy = f'{random_proxy.protocol}://{random_proxy.ip}:{random_proxy.port}'

        try:
            response = s.get(urls[0], timeout=4, proxies=proxy)
            error = 'The specified profile could not be found'

            with self.print_lock:
                if error in response.text:
                    self.log_result(word, "id", "available")
                else:
                    self.log_result(word, "id", "taken")
        except Exception:
            print("Request failed.")

        try:
            response = s.get(urls[1], timeout=4, proxies=proxy)
            error = 'No group could be retrieved for the given URL'

            with self.print_lock:
                if error in response.text:
                    self.log_result(word, "group", "available")
                else:
                    self.log_result(word, "group", "taken")
        except Exception:
            print("Request failed.")

    def threader(self):
        while True:
            item = self.queue.get()
            self.parse_job(item)
            self.queue.task_done()

    def check(self):
        start = time.time()

        for x in range(0, self.thread_count):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()

        for item in range(self.words.__len__()):
            self.queue.put(item)

        self.queue.join()

        total = str(time.time() - start)
        print(f'Checked {self.words.__len__()} words in {total} seconds.')

