#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as r

import settings
import subprocess
import os
import os.path

# !/usr/bin/env python
import sys
import os
import glob
from analize_logging import logger, logging_file
from pydub import AudioSegment
import upload_s3

"""
LIN　BOTから送信された音声データをmp3に変換し、m4a_files/配下にアップロードするところまで担当する
"""
KEY1 = settings.SONIC_API_KEY

# 音声ファイルをmp3に変換
def m4a_to_mp3(input_file_path):
    # パスから、拡張子と名前を分ける
    root, ext = os.path.splitext(input_file_path)
    logger.info('start m4a to mp3 convert {}'.format(input_file_path))
    upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'mico/log/{}'.format(logging_file))
    if ext not in ['.m4a', '.mp4']:
        logger.debug('input file: {}'.format(str(input_file_path)))
        return
    if os.path.exists('/tmp/') is not True:
        logger.info('make directory to mp3_files')
        upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'mico/log/{}'.format(logging_file))
        os.mkdir('/tmp/')
    # 変換するmp3ファイルの名前
    input_file_path_mp3 = '%s.mp3' % root
    # set commands for m4a to mp3 using ffmpeg
    cmd = 'ffmpeg -i %s -ab 64k -ar 16000 %s' % (input_file_path, input_file_path_mp3)
    upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'mico/log/{}'.format(logging_file))
    logger.info('converted mp3 file: {}'.format(input_file_path_mp3))
    logger.info(cmd)
    # do m4a to mp3（どちらもバイナリではなくパスを指定すること)
    status, output = subprocess.getstatusoutput(cmd)
    if status != 0:
        logger.error('failed convert {0}, {1}'.format(status, output))
        return input_file_path_mp3
    # S3にアップロード
    upload_s3.sign_s3(input_file_path_mp3, 'mico/mp3/{}.mp3'.format(root.strip('/tmp/')))
    logger.info('Done converted\nstatus: {0}\noutput: {1}'.format(status, output))
    upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'mico/log/{}'.format(logging_file))
    # 保存
    # with open(input_file_path_mp3, 'rw') as fb:
    #     fb.write(input_file_path_mp3)
    # # mp3ファイルを5分にカットする
    # mp3 = AudioSegment.from_file(input_file_path_mp3, format='mp3')
    # # 0~500sec(300000ms)にカット
    # mp3_5min = mp3[0:300000]
    # mp3ファイルパスを返す
    return input_file_path_mp3


if __name__ == "__main__":
    reply_token = 'dummy'
    input_file_name = 'tmp/123456yuiop90.mp4'
    m4a_to_mp3(input_file_name)