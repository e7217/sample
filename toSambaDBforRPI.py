# -*- coding: utf-8 -*-
# 위의 주석 건들지 말 것.
import csv
import os
import time
import glob
import shutil
import pymssql
import datetime


def CSV2list(filename):  # CSV파일을 리스트화

    try:
        with open(filename, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

            CSVlist = []
            for row in csvreader:
                CSVlist.append(row)

        return CSVlist
    except IOError:
        print 'exist no file'


def removefile(file1, file2):
    os.unlink(file1)  # file1 삭제
    os.unlink(file2)  # file2 삭제
    print 'remove complete'


def removedir():
    date_ = str(datetime.datetime.now().date().year)[2:] + ('0' + str(datetime.datetime.now().date().month))[-2:] + (
                                                                                                                            '0' + str(
                                                                                                                        datetime.datetime.now().date().day))[
                                                                                                                    -2:]
    print 'removedir: ', date_
    list = glob.glob(os.getcwd() + '/EXPORT/*/*')
    for fn in list:
        if not date_ in fn:
            print fn
            shutil.rmtree(fn, True)


def copyfile(file):
    time.sleep(10)  # 복사 전 딜레이 - 원본 작성이 완료되기를 기다림.
    try:
        # if original_glob()[0][-8:]=='WAVE.csv':
        #     os.unlink(original_glob()[0])
        #     print 'remove etc file'
        #
        # elif original_glob()[0][-8:]=='DATA.csv':
        #     time.sleep(1)
        #     x = os.getcwd()+'/EXPORT/*/copy/'

        shutil.copy(file, os.getcwd() + '/EXPORT/')
        print 'copy complete'
    except:
        print 'copy failed'
    return


def original_glob():
    # 현재날짜 리턴
    date_ = str(datetime.datetime.now().date().year)[2:] + ('0' + str(datetime.datetime.now().date().month))[:2] + str(
        datetime.datetime.now().date().day)
    # 현재시간 리턴
    time_ = str(datetime.datetime.now().time().hour)
    return glob.glob(os.getcwd() + '/EXPORT/*/*/*/' + '*DATA.csv')  # 원본 .csv파일 탐색경로


def destination_glob():
    return glob.glob(os.getcwd() + '/EXPORT/*.csv')  # 해당 경로로 복사한 파일 조회하여 리턴


def selfile(filelist):  # 가장 오래된 파일경로 리턴
    s1 = filelist  # 파일 목록
    selfile = ''
    x = 100000000000
    for fn in s1:
        ctime = os.path.getctime(fn)
        # print 'ctime: ',ctime
        if ctime < x:
            x = ctime
            selfile = fn
    return selfile


def initialize():
    with open("connect_env.txt", 'r') as fr:
        buf_lines = fr.readlines()
        server = buf_lines[0:1][0].replace('server = ', '')[:-2]
        user = buf_lines[1:2][0].replace('user = ', '')[:-2]
        password = buf_lines[2:3][0].replace('password = ', '')[:-2]
        database = buf_lines[3:4][0].replace('database = ', '')[:-2]
        mchcd = (buf_lines[4:5][0].replace('machine = ', ''))[:-2]
    return server, user, password, database, mchcd


def outputlist(table):
    with open('output.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(table)
        print 'write data to logfile.'


def Errlist(msg):
    with open('Err.txt', 'a') as f:
        f.write(msg)
        f.write(str(datetime.datetime.now()))
        f.write('\n')


while True:
    # time.sleep(1)                                                      # 명령이 일어나는 주기
    s = time.time()
    try:

        server, user, password, database, mchcd = initialize()  # 접속변수 설정 - 텍스트 환경설정에서 불러오기
        selectfile = selfile(original_glob())
        copyfile(selectfile)  # 원본 파일을 복사용 폴더로 복사.
        # os.rename(selectfile,selectfile+'bak')
        targetFile = selfile(destination_glob())  # 파싱 작업을 할 대상파일 설정 - 생성날짜 오름차순
        data = CSV2list(targetFile)[1]  # 데이터만 추출
        date = targetFile.replace(os.getcwd() + '/EXPORT', '')  # 날짜시간 추출
        date = date[1:14]
        data.insert(0, mchcd)  # 데이터에 머신코드 추가
        # data.insert(1,date)                                            # 데이터에 날짜시간 추가
        print 'file: ', targetFile
        print 'data: ', data

        ######################################################
        conn = pymssql.connect(server, user, password, database)  # DB 서버에 연결
        cursor = conn.cursor()

        # 저장 프로시저
        cursor.callproc('usp_toSambaDBt', data)
        cursor.nextset()

        cursor.close()
        conn.commit()
        conn.close()

        e = time.time()
        # print 'totaltime: ', e-s
        #####################################################
        outputlist(data)
        # os.rename(selectfile,selectfile+'bak')
        # os.rename(targetFile,targetFile+'bak')
        ### remove process start
        removefile(selectfile, targetFile)  # 해당파일과 복사파일 삭제
        removedir()
        # print 'removdir: ', glob.glob(os.getcwd() + '/EXPORT/*/*/*/*WAVE.csv')
        # os.unlink(os.getcwd() + '/EXPORT/*/*/*/*WAVE.csv')
        ### remove process end



    except IndexError:  # 복사할 파일이 없어서 멈추는 경우 무시
        e = time.time()
        print 'IndexE'
        Errlist('IndexE, ')
        # print 'totaltime: ', e - s
        continue
    except TypeError:
        e = time.time()
        print 'TypeE'
        Errlist('TypeE, ')
        # print 'totaltime: ', e - s
        continue
    except OSError:
        print 'oeE'
        # Errlist('WindowE, ')
        e = time.time()
        # print 'totaltime: ', e - s
        continue
    except pymssql.OperationalError:
        print 'pymssql.operationE'
        Errlist('pymssql.operationE, ')
        continue
    # except pymssql.DatabaseError
