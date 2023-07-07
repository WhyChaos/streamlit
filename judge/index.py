import os
import streamlit as st


class Judge:
    def __init__(self, keywords):
        self.keywords = keywords.split()

    def main(self, word: str):
        for keyword in self.keywords:
            if keyword in word:
                return True
        return False
