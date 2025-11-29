import os
import tkinter.messagebox as tkmb
from tkinter import Menu
import customtkinter as ctk
from app import flask_app as api_app
from .api import database

with api_app.test_client() as client:
    response = client.get("/select/gov_website")
    print(response.get_json())