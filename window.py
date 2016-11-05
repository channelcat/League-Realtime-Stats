import gevent
import tkinter as tk
import pygubu
import pygubu.builder.ttkstdwidgets

from threading import Thread
from gui import GUI

class Gui(object):
    def __init__(self, title, kill_event):
        self.greenlet = None
        self.root = tk.Tk()
        self.kill_event = kill_event
        self.root.wm_title(title)

        self.builder = builder = pygubu.Builder()
        self.builder.add_from_string(GUI)
        self.mainwindow = self.builder.get_object('mainwindow', self.root)

        self.m_status_server = self.builder.get_object('status_server', self.root)
        self.m_status_game = self.builder.get_object('status_game', self.root)
        self.m_status_stats = self.builder.get_object('status_stats', self.root)
        self.m_status_clients = self.builder.get_object('status_clients', self.root)

        self.m_stats_player_kills = self.builder.get_object('player_kills', self.root)
        self.m_stats_player_deaths = self.builder.get_object('player_deaths', self.root)
        self.m_stats_player_assists = self.builder.get_object('player_assists', self.root)
        self.m_stats_player_cs = self.builder.get_object('player_cs', self.root)
        self.m_stats_team_kills = self.builder.get_object('team_kills', self.root)
        self.m_stats_team_deaths = self.builder.get_object('team_deaths', self.root)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.kill_event.set()
        self.root.quit()

    def start(self):
        main_thread = Thread(target=self.loop)
        main_thread.start()

    def loop(self):
        while not self.kill_event.is_set():
            self.root.update()
            gevent.sleep(0.01)


    def set_status_server(self, status):
        if self.kill_event.is_set():
            return

        self.builder.get_variable('status_server').set('true' if status else 'false')


    def set_status_game(self, status):
        if self.kill_event.is_set():
            return

        self.builder.get_variable('status_game').set('true' if status else 'false')

    def set_status_stats(self, status):
        if self.kill_event.is_set():
            return

        self.builder.get_variable('status_stats').set('true' if status else 'false')

    def set_status_clients(self, total):
        if self.kill_event.is_set():
            return

        self.m_status_clients.config(text=str(total))

    def set_stats(self, stats):
        if self.kill_event.is_set():
            return

        self.m_stats_player_cs.config(text=str(stats.get('CS', '?')))
        self.m_stats_player_kills.config(text=str(stats.get('kills', '?')))
        self.m_stats_player_deaths.config(text=str(stats.get('deaths', '?')))
        self.m_stats_player_assists.config(text=str(stats.get('assists', '?')))
        self.m_stats_team_kills.config(text=str(stats.get('team_kills', '?')))
        self.m_stats_team_deaths.config(text=str(stats.get('team_deaths', '?')))