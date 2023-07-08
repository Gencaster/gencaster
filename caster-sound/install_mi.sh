#!/bin/sh

wget https://github.com/v7b1/mi-UGens/releases/download/v0.0.4/mi-UGens-Linux.zip

unzip mi-UGens-Linux.zip

cp -R mi-UGens/ /usr/local/share/SuperCollider/Extensions

# clean up
rm -rf mi-UGens
rm -rf mi-UGens-Linux.zip
