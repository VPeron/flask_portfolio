#!/bin/bash

# Create a new migration script
flask db init
flask db migrate -m "Initial database setup"
flask db upgrade
