#!/bin/bash

ps -eo pid,%cpu --sort=-%cpu | head -n 6