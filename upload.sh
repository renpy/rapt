#!/bin/bash

# Uploads things to our website.
rsync -r doc/_build/html/ pygame@erika:/home/pygame/WWW
rsync -r dl/ pygame@erika:/home/pygame/WWW/dl
