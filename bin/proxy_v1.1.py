# coding=gbk

import io, sys, time, re, os
import winreg

xpath = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"


def setProxy(enable,proxyIp,IgnoreIp):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, xpath, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, enable)
        winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxyIp)
        winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, IgnoreIp)
    except Exception as e:
        print("ERROR: " + str(e.args))


def set_proxy(ip):
    # proxyIP = "[2001:da8:207:e055:4b5b:3c68:ec44:2c9e]:39001"
    print(ip)
    proxyIP = ip
    # IgnoreIp = "172.*;192.*;"
    IgnoreIp = "127.0.0.*"
    print(" Setting proxy")
    setProxy(1,proxyIP,IgnoreIp)
    # print(" Setting success")


def clear_proxy():
    setProxy(0,"","")


def main():
    try:
        fr = open('ipconfig.txt')
        lines = fr.readlines()
        fr.close()
        instruction_dic = {
        }
        i = 0
        for l in lines:
            i += 1
            ip = l.split('\n')[0]
            instruction_dic[i] = ip
        while 1:
            print 'No:%s\t'%(0)+'clear vpn'
            for i in range(len(instruction_dic)):
                i += 1
                print 'No:%s\tip:%s'%(i,instruction_dic[i])
            try:
                no = input('Please input a number(0-%s):'%len(instruction_dic))
            except:
                print 'input error'
                no = None
                pass
            if no == 0:
                clear_proxy()
                print 'clean vpn success'
                # os.system('pause')
            else:
                try:
                    clear_proxy()
                    ip = instruction_dic[no]
                    set_proxy(ip)
                    print 'set %s success'%(ip)

                except:
                    print 'input error'
                    # os.system('pause')
            for i in range(5):
                print('*' * 50)
    except Exception as e:
        print e
        for i in range(10):
            print('*'*10)

if __name__ == '__main__':
    main()