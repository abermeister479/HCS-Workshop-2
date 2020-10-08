#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

response = requests.get("https://google.com/search?q=dog")
soup = BeautifulSoup(response.content, "html.parser")
print(soup.prettify())
