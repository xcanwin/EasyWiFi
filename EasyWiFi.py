#!/usr/bin/env python
# -- coding: utf-8 --

import os, re, time, subprocess

def wlanConfigure(interface, profile, ssid, password):
    # 配置wifi与密码
    cmdOut = runCmd('netsh wlan show profiles')
    if re.search(u'用户配置文件\s+:', cmdOut):
        profiles = re.findall(u'用户配置文件\s+:\s+(.*?)\r\n', cmdOut)
        if profile in profiles:
            return ''
    profileFileName = '%s-%s.xml' % (interface, profile)
    xxx = 'auto' #'manual'
    profileXml = '''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>%s</name>
    <SSIDConfig>
        <SSID>
            <name>%s</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>%s</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>%s</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>
''' % (profile, ssid, xxx, password)
    file(profileFileName.encode('gbk'), 'wb').write(profileXml)
    print '[.] Configure wlan:', ssid
    runCmd('netsh wlan add profile "%s" "%s"' % (profileFileName, interface))
    os.remove(profileFileName)

def wlanConnect(interface, profile, ssid):
    # 连接指定wifi
    print '[.] Try to connect:', ssid
    runCmd('netsh wlan connect "%s" "%s" "%s"' % (profile, ssid, interface))

def getInterface(i = 0):
    # 获取无线网卡名称
    cmdOut = runCmd('netsh wlan show interfaces')
    if re.search(u'GUID', cmdOut):
        interfaces = re.findall(u'名称\s+:\s+(.*?)\r\n', cmdOut)
        print '[+] Found interfaces:', ', '.join(interfaces).encode('utf-8')
        interface = interfaces[i]
        return interface
    else:
        print '[-] Not found interface'
        exit(0)

def isConnected(ssid):
    # 判断是否连接上了指定wifi
    cmdOut = runCmd('netsh wlan show interfaces')
    if re.search(u'状态\s+:\s+已连接', cmdOut):
        connectedSsid = re.findall(u'SSID\s+:\s+(.*?)\r\n', cmdOut)[0]
        if connectedSsid == ssid:
            print '[+] Connected to wireless network:', connectedSsid
            return connectedSsid
    return None

def runCmd(cmd):
    # 执行命令
    cmd = cmd.encode('gbk')
    # print cmd
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, \
                        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return ( proc.stdout.read() + proc.stderr.read() ).decode('gbk')

def start(interface, ssid, password, intervalTime):
    # 入口
    if not interface:
        interface = getInterface()
    profile = ssid
    wlanConfigure(interface, profile, ssid, password)
    while True:
        if isConnected(ssid):
            break
        wlanConnect(interface, profile, ssid)
        time.sleep(0.5)
        if isConnected(ssid):
            break
        time.sleep(intervalTime)


if __name__ == '__main__':
    intervalTime = 3
    interface = ''
    ssid = 'wifiname'
    password = 'wifipassword'

    start(interface, ssid, password, intervalTime)
