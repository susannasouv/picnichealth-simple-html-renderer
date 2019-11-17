#!/bin/bash 

for file in $HOME/picnichealth_simple_html_renderer/**/test*html; do echo $file && cat $file | python3 simple_html_renderer/simple_html_render.py; done

