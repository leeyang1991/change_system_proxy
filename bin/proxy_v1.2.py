# coding=gbk
import os
import re

def regIESettings(op, noLocal=False, ip='', pac=''):
    '''
        # 根据需求生成Windows代理设置注册表的.reg文件内容
        # DefaultConnectionSettings项是二进制项
        # 而具体这个二进制文件怎么解析，在收藏的PDF中有详细解释。
    '''
    if not op : return
    # 如果是设置IP代理的模式 则检查IP地址的有效性(允许为空，但不允许格式错误)
    if 'Proxy' in op and not ip == '':
        # if len(extractIp(ip))==0
        if 1 > len(re.findall('([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s*:{0,1}\s*([0-9]{1,5}){0,1}',ip)) :
            # print '---Unexpected IP Address:%s---'%ip
            return
    options = {'On':'0F','Off':'01','ProxyOnly':'03','PacOnly':'05','ProxyAndPac':'07','D':'09','DIP':'0B','DS':'0D'}
    if op == 'Off':
        reg_value = '46,00,00,00,00,00,00,00,01'
    else:
        switcher = options.get(op)
        if not switcher:
            # print '\n---Unexpected Option. Please check the value after [-o]---\n'
            return
        skipLocal = '07,00,00,00,%s'%__toHex('<local>') if noLocal else '00'
        reg_value = '46,00,00,00,00,00,00,00,%(switcher)s,00,00,00,%(ipLen)s,00,00,00,%(ip)s00,00,00,%(skipLocal)s,21,00,00,00%(pac)s' % ({ 'switcher':switcher,'ipLen':__toHex(len(ip)),'ip':__toHex(ip)+',' if ip else '','infoLen':__toHex(len('<local>')),'skipLocal':skipLocal,'pac':','+__toHex(pac) if pac else '' })
    settings = 'Windows Registry Editor Version 5.00\n[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections]\n"DefaultConnectionSettings"=hex:%s' % reg_value
    # print 'Using proxy address: %s' % ip
    # print op, ip, pac
    # print options[op] +'\n'+ __toHex(ip) +'\n'+ __toHex(pac)
    # print settings
    # === 生成reg文件并导入到注册表中 ===
    filePath = '%s\DefaultConnectionSettings.reg'%os.getcwd()
    with open(filePath, 'w') as f:
        f.write( settings )
    cmd = 'reg import "%s"' %filePath

    result = os.popen(cmd)
    # os.remove('%s\DefaultConnectionSettings.reg' % os.getcwd())
    if len(result.readlines()) < 2 :
        pass
        # print '---Successfully import proxy into Registry on this machine.---'
    return

def __toHex(obj):
    if obj == '': return ''
    elif obj == 0 or obj == '0' or obj == '00': return '00'
    if isinstance(obj, str):
        rehex = [str(hex(ord(s))).replace('0x','') for s in obj]
        return ','.join(rehex)
    elif isinstance(obj, int):
        num = str(hex(obj)).replace('0x', '')
        return num if len(num)>1 else '0'+num # 如果是一位数则自动补上0，7为07，e为0e



def clear_proxy():
    regIESettings(op='Off')


def set_proxy(ip):
    proxyIP = ip
    cmd = 'sysproxy.exe global '+proxyIP+' localhost;192.*;127.*'
    os.system(cmd)

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
            for i in range(3):
                print('*' * 50)
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
            for i in range(3):
                print('*' * 50)
            os.system('cls')
    except Exception as e:
        print e
        for i in range(10):
            print('*'*10)

if __name__ == '__main__':
    main()