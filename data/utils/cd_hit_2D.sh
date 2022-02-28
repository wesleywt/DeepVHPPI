#!/bin/bash
echo "Running CD-HIT"
/home/wesleywt/anaconda3/bin/cd-hit-2d cd-hit-2d -i hidb_human_positive.fasta -i2 hidb_human_negative.fasta -o hidb_human_negative_novel -c 0.8 -n 5 -d 0 -M 16000 -T 8
