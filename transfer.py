#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Binux <roy@binux.me>
#
# Distributed under terms of the MIT license.

"""
change the role of user
"""

import sys
import sqlite3_db
import db

source_user_db = sqlite3_db.UserDB()
target_user_db = db.UserDB()
source_task_db = sqlite3_db.TaskDB()
target_task_db = db.TaskDB()
source_tpl_db = sqlite3_db.TPLDB()
target_tpl_db = db.TPLDB()

user_id = 1
tpl_id = 1
task_id = 35

for task in source_task_db.list(user_id, fields="*"):
    task_id = task['id']
    user_id = task['userid']

    init_env = source_user_db.decrypt(user_id, task['init_env'])
    print task_id, init_env, 'task ok...'
    init_env = target_user_db.encrypt(user_id, init_env)

    target_task_db.mod(task_id, init_env=init_env, env=None, session=None, note=task.get('note'))

tpl_list = source_tpl_db.list("*")
for tpl in tpl_list:
    tpl_id = tpl['id']
    if not tpl['userid']:
        continue
    user_id = tpl['userid']

    tpl['har'] = source_user_db.decrypt(user_id, tpl['har'])
    tpl['tpl'] = source_user_db.decrypt(user_id, tpl['tpl'])

    har = target_user_db.encrypt(user_id, tpl['har'])
    tpl = target_user_db.encrypt(user_id, tpl['tpl'])

    target_tpl_db.mod(tpl_id, har=har, tpl=tpl)
    print tpl_id, 'tpl ok...'
