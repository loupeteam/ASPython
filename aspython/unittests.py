"""HTTP client for the on-PLC unit-test server."""
import logging
import os.path

import requests


class UnitTestServer:
    def __init__(self, host: str = 'http://127.0.0.1', destination: str = './TestResults'):
        self._host = host
        self._destination = destination
        self.connected = False
        self.testSuites = []
        try:
            r = requests.get(url=self._host + '/WsTest/?', params={})
            if r.status_code == 200:
                data = r.json()
                self.testSuites = data['itemList']
                self.connected = True
            else:
                logging.error(f'Received HTTP response {r.status_code} from the test server')
        except Exception as e:
            logging.error(f'Exception occurred while connecting to the test server ({e})')

    def runTest(self, name: str):
        for testSuite in self.testSuites:
            if testSuite['device'] == name:
                r = requests.get(url=self._host + '/WsTest/' + name, params={})
                if r.status_code == 200:
                    with open(f'{os.path.join(self._destination, name)}.xml', 'w') as f:
                        f.write(r.text)
