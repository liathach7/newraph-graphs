#!/bin/bash
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - newton_graphs2:app