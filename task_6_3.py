import logging
import sys
import re
import lxml
import json
import asyncio
import aiohttp


__author__ = "Andrew Gafiychuk"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("[+]App started...")