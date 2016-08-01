#!/usr/bin/python

import GrafanaJSON
import pprint


board = GrafanaJSON.Dashboard('TestTitle', tags=['generated'])
target = GrafanaJSON.Target('test.host.com', 'ping')
target.add_tag('cmd', 'ping')
target.add_tag('metric', 'rta')
board.add_row()
board.add_panel(targets=[target])
pprint.pprint(board.get())
