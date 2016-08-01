#!/usr/bin/python

import copy
import json


json_dashboard_template = {
    "id": None,
    "title": None,
    "tags": [],
    "rows": [],
    "schemaVersion": 12,
    "version": 3
}
json_row_template = {'panels': [], 'title': 'row'}
json_panel_template = {'title': '', 'type': 'graph', "span": 12, 'height': '200px', 'id': 0, 'targets': [],
                       'linewidth': 1, 'yaxes':
                           [
                               {"format": "short", "label": "", "logBase": 1, "max": None, "min": 0, "show": True},
                               {"format": "short", "label": "", "logBase": 1, "max": None, "min": None, "show": True}
                           ]
                       }
json_target_template = {
    "dsType": "influxdb",
    'measurement': None,
    'tags': [],
    'alias': '',
    'aliasColors': {}
}


class Dashboard(object):

    def __init__(self, title, tags=[]):
        self.dashboard = copy.deepcopy(json_dashboard_template)
        self.dashboard['title'] = title
        self.dashboard['tags'] = tags
        self.rows = []
        self.last_id = 1

    def add_row(self):
        self.rows.append(copy.deepcopy(json_row_template))

    def add_panel(self, row=-1, span=12, height=200, targets=[], value_format=None):
        if len(self.rows) == 0:
            self.add_row()
        panel = copy.deepcopy(json_panel_template)
        panel['span'] = span
        panel['height'] = str(height)+'px'
        panel['id'] = self.last_id
        self.last_id += 1
        for target in targets:
            panel['targets'].append(target.get())
        if value_format:
            panel['yaxes'][0]['format'] = value_format
        self.rows[row]['panels'].append(panel)
        return self.last_id

    def get_json(self):
        self.dashboard['rows'] = self.rows
        return json.dumps({'dashboard': self.dashboard, 'overwrite': True})

    def get(self):
        self.dashboard['rows'] = self.rows
        return {'dashboard': self.dashboard, 'overwrite': True}


class Target(object):

    def __init__(self, measurement, alias=''):
        self.target = copy.deepcopy(json_target_template)
        self.target['measurement'] = measurement
        self.target['alias'] = alias

    def add_tag(self, key, value, operator='=', condition='AND'):
        if len(self.target['tags']) == 0:
            tag = {'key': key, 'value': value, 'operator': operator}
        else:
            tag = {'key': key, 'value': value, 'operator': operator, 'condition': condition}
        self.target['tags'].append(tag)

    def get(self):
        return self.target


