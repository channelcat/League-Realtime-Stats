GUI = """<?xml version='1.0' encoding='utf-8'?>
<interface>
  <object class="ttk.Frame" id="mainwindow">
    <property name="height">200</property>
    <property name="padding">10</property>
    <property name="width">200</property>
    <layout>
      <property name="column">0</property>
      <property name="propagate">True</property>
      <property name="row">0</property>
    </layout>
    <child>
      <object class="ttk.Labelframe" id="status_frame">
        <property name="height">200</property>
        <property name="padding">5</property>
        <property name="text" translatable="yes">Status</property>
        <property name="width">200</property>
        <layout>
          <property name="column">0</property>
          <property name="columnspan">2</property>
          <property name="propagate">True</property>
          <property name="row">3</property>
        </layout>
        <child>
          <object class="ttk.Label" id="Label_1">
            <property name="text" translatable="yes">Clients:</property>
            <layout>
              <property name="column">4</property>
              <property name="padx">5</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="status_clients">
            <property name="text" translatable="yes">123</property>
            <layout>
              <property name="column">5</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Checkbutton" id="status_server">
            <property name="offvalue">false</property>
            <property name="onvalue">true</property>
            <property name="state">disabled</property>
            <property name="text" translatable="yes">Server</property>
            <property name="variable">string:status_server</property>
            <layout>
              <property name="column">0</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Checkbutton" id="status_game">
            <property name="offvalue">false</property>
            <property name="onvalue">true</property>
            <property name="state">disabled</property>
            <property name="text" translatable="yes">Game</property>
            <property name="variable">string:status_game</property>
            <layout>
              <property name="column">1</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Checkbutton" id="status_stats">
            <property name="offvalue">false</property>
            <property name="onvalue">true</property>
            <property name="state">disabled</property>
            <property name="text" translatable="yes">Stats</property>
            <property name="variable">string:status_stats</property>
            <layout>
              <property name="column">2</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
      </object>
    </child>
    <child>
      <object class="ttk.Labelframe" id="Labelframe_2">
        <property name="height">200</property>
        <property name="padding">5</property>
        <property name="text" translatable="yes">Player</property>
        <property name="width">200</property>
        <layout>
          <property name="column">0</property>
          <property name="padx">0 5</property>
          <property name="propagate">True</property>
          <property name="row">4</property>
        </layout>
        <child>
          <object class="ttk.Label" id="Label_7">
            <property name="text" translatable="yes">Kills:</property>
            <layout>
              <property name="column">0</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="player_kills">
            <property name="text" translatable="yes">123</property>
            <layout>
              <property name="column">1</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="Label_9">
            <property name="text" translatable="yes">  Deaths:</property>
            <layout>
              <property name="column">2</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="player_deaths">
            <property name="text" translatable="yes">123</property>
            <layout>
              <property name="column">3</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="Label_11">
            <property name="text" translatable="yes">  Assists:</property>
            <layout>
              <property name="column">4</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="player_assists">
            <property name="text" translatable="yes">123</property>
            <layout>
              <property name="column">5</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="Label_13">
            <property name="text" translatable="yes">  CS:</property>
            <layout>
              <property name="column">6</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="player_cs">
            <property name="text" translatable="yes">123</property>
            <layout>
              <property name="column">7</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
      </object>
    </child>
    <child>
      <object class="ttk.Labelframe" id="Labelframe_4">
        <property name="height">200</property>
        <property name="padding">5</property>
        <property name="text" translatable="yes">Team</property>
        <layout>
          <property name="column">1</property>
          <property name="propagate">True</property>
          <property name="row">4</property>
        </layout>
        <child>
          <object class="ttk.Label" id="Label_3">
            <property name="text" translatable="yes">Kills: </property>
            <layout>
              <property name="column">0</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="team_kills">
            <property name="text" translatable="yes">123</property>
            <layout>
              <property name="column">1</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="Label_4">
            <property name="text" translatable="yes">Deaths</property>
            <layout>
              <property name="column">2</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
        <child>
          <object class="ttk.Label" id="team_deaths">
            <property name="text" translatable="yes">123</property>
            <layout>
              <property name="column">3</property>
              <property name="propagate">True</property>
              <property name="row">0</property>
            </layout>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
"""