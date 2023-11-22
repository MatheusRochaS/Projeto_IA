import requests

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YzQ1YjMwMzI2ZTAzYjI1NmZmOTcyYjQxYzVmNWE3NCIsInN1YiI6IjY1M2FlOTdlNTE5YmJiMDBhYjY3NjJkNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FyIL9T3Sg9A-n2LClwc-juRjEpwLHLUpAv58Tx-mvdQ"
}

class request:
    def __init__(self):
        self.header = headers

    def get(url):
        response = requests.get(url, headers=headers)
        return response.json()
    
    def post(self, url, data):
        response = requests.get(url, headers=self.header, data=data)
        return response.text
    
    def put(self, url, data):
        response = requests.get(url, headers=self.header, data=data)
        return response.text
    
    def delete(self, url):
        response = requests.get(url, headers=self.header)
        return response.text