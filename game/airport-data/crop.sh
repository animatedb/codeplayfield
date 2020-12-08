#!/bin/bash

ffmpeg -i "production ID 4395200.mp4" -ss 00:00:52 -t 00:00:04 -vcodec copy -acodec copy bird-flight.mp4

