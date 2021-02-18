import socket
import subprocess
import tkinter


def check_online(function):
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except ConnectionResetError:
            start.close()
        except OSError:
            start.close()
    return wrapper


class Window:
    def __init__(self):
        self.__net_data = self.__NetData()
        self.__root = tkinter.Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.__exit)
        self.__root.title('Online Volume Control')
        self.__root.geometry('+200+500')
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect_frame = tkinter.Frame(self.__root)
        self.__control_frame = tkinter.Frame(self.__root)

        # connection frame
        self.__ip_entry = tkinter.Entry(master=self.__connect_frame, background='black', foreground='white',
                                        insertbackground='white', insertwidth=1, font=('calibri', 20, 'bold'),
                                        justify='center', width=15)
        self.__ip_entry.insert(0, self.__net_data.host)
        self.__ip_entry.focus()

        self.__connect_button = tkinter.Button(master=self.__connect_frame, text='Connect',
                                               font=('calibri', 10, 'bold'), command=self.__login, padx=10,
                                               bg='black', fg='white', activebackground='gray')
        self.__error_label = tkinter.Label(master=self.__connect_frame, font=('calibri', 10, 'bold'),
                                           text='', foreground='red')

        # connected frame
        self.__up_button = tkinter.Button(master=self.__control_frame, text='Up', font=('calibri', 12),
                                          command=self.__up, padx=10, bg='black', fg='white',
                                          activebackground='gray', repeatdelay=500, repeatinterval=250)
        self.__down_button = tkinter.Button(master=self.__control_frame, text='Down', font=('calibri', 12),
                                            command=self.__down, padx=10, bg='black', fg='white',
                                            activebackground='gray')
        self.__mute_button = tkinter.Button(master=self.__control_frame, text='Mute', font=('calibri', 12),
                                            command=self.__mute, padx=10, bg='black', fg='white',
                                            activebackground='gray')
        self.__kill_button = tkinter.Button(master=self.__control_frame, text='Kill Zoom', font=('calibri', 12),
                                            command=self.__kill_zoom, padx=10, bg='black', fg='red',
                                            activebackground='gray')

        self.__ip_entry.pack()
        self.__connect_button.pack(pady=5)
        self.__connect_frame.pack()

    class __NetData:
        def __init__(self):
            self.host = ''
            self.port = 56789
            self.__get_host()

        def __get_host(self):
            temp = subprocess.run('arp -a', capture_output=True)
            for line in temp.stdout.decode('utf-8').split('\r'):
                if '90-4c-e5-c6-c4-89' in line:
                    self.host = line.strip().split(' ')[0]
            if self.host == '':
                self.host = 'Offline'

    def __controls(self):
        self.__connect_frame.forget()
        self.__up_button.pack(fill='x')
        self.__down_button.pack(fill='x')
        self.__mute_button.pack(fill='x')
        self.__kill_button.pack(fill='x')
        self.__control_frame.pack(expand=True, fill='both')

    def __login(self):
        def show_error(error):
            self.__error_label.config(text=f'Cant connect. {error}')
            self.__error_label.pack()

        try:
            self.__connection.connect((self.__ip_entry.get(), self.__net_data.port))
            self.__connection.send(b'ThisIsACode4334')
            data = self.__connection.recv(1024)
            if data == b'IN':
                self.__online = True
                self.__controls()
        except ConnectionRefusedError:
            show_error('Refused')
        except TimeoutError:
            show_error('Time out')
        except socket.gaierror:
            pass

    def __call__(self, *args, **kwargs):
        self.__root.mainloop()

    @check_online
    def __up(self):
        self.__connection.send(b'up')

    @check_online
    def __down(self):
        self.__connection.send(b'down')

    @check_online
    def __mute(self):
        self.__connection.send(b'mute')

    @check_online
    def __kill_zoom(self):
        self.__connection.send(b'zoom')

    @check_online
    def __exit(self):
        self.__connection.send(b'exit')
        self.__connection.close()
        self.__root.destroy()

    def close(self):
        self.__root.destroy()


if __name__ == '__main__':
    start = Window()
    start()
