import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import *
from PyQt5 import uic



class GUI(QMainWindow):
    def __init__(self):
        self.port = serport()
        super(GUI,self).__init__()
        uic.loadUi('Design.ui',self)
        self.show()
        
        self.Button_Send_AT.clicked.connect(lambda: self.Send_Message('AT'))
        self.Button_Reset.clicked.connect(lambda: self.Send_Message('AT+RESET'))
        self.Button_Version.clicked.connect(lambda: self.Send_Message('AT+VERSION?',2))
        self.Button_Restore_Default.clicked.connect(lambda: self.Send_Message('AT+ORGL'))
        self.Button_Address.clicked.connect(lambda: self.Send_Message('AT+ADDR?',2))
        # Need to add case statements for these functions:
        self.Button_Check_Module_Name.clicked.connect(lambda: self.Send_Message('AT+NAME?',2))
        self.Button_Get_Device_Name.clicked.connect(lambda: self.notWork())#self.Send_Message(f'AT+RNAME?{self.Label_Get_Address.text().replace(":",",")}',2))
        self.Button_Check_Module_Mode.clicked.connect(lambda: self.Send_Message('AT+ROLE?',2))
        self.Button_Check_Device_Class.clicked.connect(lambda: self.Send_Message('AT+CLASS?',2))
        self.Button_Check_GIAC.clicked.connect(lambda: self.Send_Message('AT+IAC?',2))
        self.Button_Check_Query_Access.clicked.connect(lambda: self.Send_Message('AT+INQM?',2))
        self.Button_Check_Pin_Code.clicked.connect(lambda: self.Send_Message('AT+PSWD?',2))
        self.Button_Check_Serial.clicked.connect(lambda: self.Send_Message('AT+UART?',2))
        self.Button_Check_Connect_Mode.clicked.connect(lambda: self.Send_Message('AT+CMODE?',2))
        self.Button_Check_Fixed_Address.clicked.connect(lambda: self.Send_Message('AT+BIND?',2))
        self.Button_Check_LED_IO.clicked.connect(lambda: self.Send_Message('AT+POLAR?',2))
        self.Button_Check_Scan_Parameter.clicked.connect(lambda: self.Send_Message('AT+IPSCAN?',2))
        self.Button_Check_SHIFF_Parameter.clicked.connect(lambda: self.Send_Message('AT+SNIFF?',2))
        self.Button_Check_Security_Mode.clicked.connect(lambda: self.Send_Message('AT+SENM?',2))
        self.Button_Get_Auth_Device_Count.clicked.connect(lambda: self.Send_Message('AT+ADCN?',2))
        self.Button_Recent_Used_Auth_Device.clicked.connect(lambda: self.Send_Message('AT+MRAD?',2))
        self.Button_Get_Module_Working_State.clicked.connect(lambda: self.Send_Message('AT+STATE?',2))
        
        
        # Need to add case statements for these functions
    def notWork(self):
        print('This instruction not work yet...')
    def Send_Message(self,cmd,length=1):
        print(f'Sending cmd: {cmd}')
        cmd = cmd + '\r\n'
        cmd = cmd.encode('UTF-8')
        self.port.write(cmd)
        string = ''
        for i in range(1,length+1):
            string = f'{string}{self.port.readline().decode("UTF-8")}'
        print(f'Reponse cmd: {string}')
        match cmd:
            case b'AT\r\n':
                if(string == 'OK\r\n'):
                    self.Label_Send_AT.setText(f'Good')
                    self.Label_Send_AT.setStyleSheet("color: green;")
                else:
                    self.Label_Send_AT.setText(f'Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
                    self.Label_Send_AT.setStyleSheet("color: red;")
            case b'AT+RESET\r\n':
                if(string == 'OK\r\n'):
                    self.Label_Reset.setText(f'Good')
                    self.Label_Reset.setStyleSheet("color: green;")
                else:
                    self.Label_Reset.setText(f'Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
                    self.Label_Reset.setStyleSheet("color: red;")
            case b'AT+VERSION?\r\n':
                response = string.split(':')
                version_response = response[1].split('\r')
                version = version_response[0]
                OK_response = response[1].split('\n')
                if(OK_response[1] == 'OK\r'):
                    print('Good')
                    print(f'Firmware Version: {version}')
                    self.Label_Version.setText(f'Version: {version}')
                else:
                    print('Fail')
                    self.Label_Version.setText(f'Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
                    self.Label_Version.setStyleSheet("color: red;")
            case b'AT+ORGL\r\n':
                if(string == 'OK\r\n'):
                    print(f'Good')
                    self.Label_Restore_Default.setText(f'Restore Default Success')
                else:
                    print('Fail')
                    self.Label_Restore_Default.setText(f'Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
                    self.Label_Restore_Default.setStyleSheet("color: red;")
            case b'AT+ADDR?\r\n':
                string_list = string.split('\n')
                line1 = string_list[0]
                line2 = string_list[1]
                line1_split = line1.split(':')
                address = ''
                for i in range(1,len(line1_split)):
                    line1_split[i] = line1_split[i].replace('\r','')
                    address = address + f'{line1_split[i]}'
                    if i != len(line1_split)-1:
                        address = address + ':'
                print(f'Address: {address}')
                if(line2 == 'OK\r'):
                    print('Good')
                    self.Label_Get_Address.setText(address)
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+NAME?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    name = response_list[1]
                    print(f'Name = {name}')
                    self.Label_Check_Module_Name.setText(name)
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+ROLE?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameter = response_list[1]
                    if(int(parameter) == 0):
                        parameter = f'Slave'
                    elif(int(parameter) == 1):
                        parameter = f'Master'
                    elif(int(parameter) == 2):
                        parameter = f'Slave-Loop'
                    print(f'parameter: {parameter}')
                    self.Label_Check_Module_Mode.setText(parameter)
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+CLASS?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameter = response_list[1].replace('\r','')
                    print(f'parameter: 0x{parameter}')
                    self.Label_Check_Device_Class.setText(f'0x{parameter}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+IAC?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameter = response_list[1].replace('\r','')
                    print(f'parameter = 0x{parameter}')
                    self.Label_Check_GIAC.setText(f'0x{parameter}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+INQM?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameters = response_list[1].split(',')
                    parameter = parameters[0].replace('\r','')
                    parameter2 = parameters[1].replace('\r','')
                    parameter3 = parameters[2].replace('\r','').replace('\n','')
                    if(parameter == '1'):
                        parameter = 'RSSI'
                    else:
                        parameter = 'Standard'
                    print(f'parameter: {parameter}')
                    print(f'Maximum Number of Bluetooth Devices to Respond to: {parameter2}')
                    print(f'Timeout: {parameter3}')
                    
                    self.Label_Query_P1.setText(f'INQ Mode: {parameter}')
                    self.Label_Query_P2.setText(f'Max Num of Devices: {parameter2}')
                    self.Label_Query_P3.setText(f'Timeout: {parameter3}')
                    
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+PSWD?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    code = response_list[1].replace('"','')
                    print(f'PIN Code (Password): {code}')
                    self.Label_Check_Pin_Code.setText(f'Password: {code}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+UART?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameters = response_list[1].split(',')
                    print(f'Baud Rate = {parameters[0]}')
                    if(parameters[1] == '0'):
                        stop_parameter = 'One Stop Bit'
                        stop_bits = 1
                    else:
                        stop_parameter = 'Two Stop Bit'
                        stop_bits = 2
                    print(stop_parameter)
                    if(parameters[2] == '0\r'):
                        parity_parameter = 'None'
                    elif(parameters[2] == '1\r'):
                        parity_parameter = 'Odd'
                    else:
                        parity_parameter = 'Even'
                    print(parity_parameter)
                    self.Label_Serial_P1.setText(f'Baud Rate: {parameters[0]}')
                    self.Label_Serial_P2.setText(f'Stop Bits: {stop_bits}')
                    self.Label_Serial_P3.setText(f'Parity: {parity_parameter}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+CMODE?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameter = response_list[1].replace('\r','')
                    if(parameter == '0'):
                        parameter = 'Connect Fixed Address'
                    elif(parameter == '1'):
                        parameter = 'Connect Any Address'
                    else:
                        parameter = 'Slave-Loop'
                    print(f'Parameter: {parameter}')
                    self.Label_Check_Connect_Mode.setText(parameter)
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+BIND?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    fix_address = response[0].replace('+BIND:','')
                    print(f'fixed address = {fix_address}')
                    self.Label_Check_Fixed_Address.setText(f'Address: {fix_address}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+POLAR?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    parameters = response[0].split(':')
                    print(f'PIO8: {parameters[1]}')
                    print(f'PIO9: {parameters[2]}')
                    self.Label_Check_LED_P1.setText(f'PIO8: {parameters[1]}')
                    self.Label_Check_LED_P2.setText(f'PIO9: {parameters[2]}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+IPSCAN?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameters = response_list[1].split(',')
                    parameters[3] = parameters[3].replace('\r','')
                    print(f'Query Time Interval: {parameters[0]}')
                    print(f'Query Duration: {parameters[1]}')
                    print(f'Paging Interval: {parameters[2]}')
                    print(f'Call Duration: {parameters[3]}')
                    self.Label_Check_Scan_P1.setText(f'Query time interval: {parameters[0]}')
                    self.Label_Check_Scan_P2.setText(f'Query duration: {parameters[1]}')
                    self.Label_Check_Scan_P3.setText(f'Paging interval: {parameters[2]}')
                    self.Label_Check_Scan_P4.setText(f'Call duration: {parameters[3]}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+SNIFF?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameters = response_list[1].split(',')
                    print(f'Max time: {parameters[0]}')
                    print(f'Min time: {parameters[1]}')
                    print(f'Retry time: {parameters[2]}')
                    print(f'Time out: {parameters[3]}')
                    self.Label_Check_SHIFF_P1.setText(f'Max time: {parameters[0]}')
                    self.Label_Check_SHIFF_P2.setText(f'Min time: {parameters[1]}')
                    self.Label_Check_SHIFF_P3.setText(f'Retry time: {parameters[2]}')
                    self.Label_Check_SHIFF_P4.setText(f'Time out: {parameters[3]}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+SENM?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameters = response_list[1].split(',')
                    if(parameters[0] == '0'):
                        p1 = '0 + off'
                    elif(parameters[0] == '1'):
                        p1 = '1 + non secure'
                    elif(parameters[0] == '2'):
                        p1 = '2 service'
                    elif(parameters[0] == '3'):
                        p1 = '3 link'
                    elif(parameters[0] == '4'):
                        p1 = 'unknown'
                    print(f'Secure Mode: {p1}')
                    if(parameters[1] == '0\r'):
                        p2 = 'off'
                    elif(parameters[1] == '1\r'):
                        p2 = 'pt to pt'
                    elif(parameters[1] == '2\r'):
                        p2 = 'pt to pt and bcast'
                    print(f'HCI ENC Mode: {p2}')
                    self.Label_Check_Security_P1.setText(f'Secure Mode: {p1}')
                    self.Label_Check_Security_P2.setText(f'HCI ENC Mode: {p2}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+ADCN?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameter = response_list[1]
                    print(f'parameter: {parameter}')
                    self.Label_Get_Auth_Device_Count.setText(f'{parameter}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+MRAD?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameter = response_list[1]
                    print(f'parameter: {parameter}')
                    self.Label_Most_Recent_Used_Auth_Device.setText(f'{parameter}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()
            case b'AT+STATE?\r\n':
                response = string.split('\n')
                if(response[1] == 'OK\r'):
                    print('Good')
                    response_list = response[0].split(':')
                    parameter = response_list[1]
                    print(f'parameter: {parameter}')
                    self.Label_Get_Module_Work_State.setText(f'{parameter}')
                else:
                    print('Fail')
                    fail_msg = QMessageBox()
                    fail_msg.setText('command fail')
                    fail_msg.exec_()

                
    
    
def main():
    app = QApplication([])
    window = GUI()
    app.exec_()
    
def serport():
        # -- Initialize Serial Ports -- #
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial()
    
    portlist = []
    for onePort in ports:
        portlist.append(str(onePort))
    if (portlist == []):
        print('COM PORTs not Found')
        return None
    else:
        print('List of the COM Ports:')
        for onePort in ports:
            print(str(onePort))
        # -- Serial Port Detection -- #
        
        
        # -- Connect to serial Port -- #
        COM = input('Enter The COM Port you want to connect: ')
        print(f"connect to COM Port: {COM}")
        Connection = serial.Serial(COM,38400,timeout=0.5)
        Connection.baudrate = 38400
        Connection.parity = 'N'
        Connection.bytesize = 8
        Connection.stopbits = 1
        return Connection
    
if __name__ == '__main__':
    main()
