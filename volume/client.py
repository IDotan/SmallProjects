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
        self.__connect_frame = self.__connection_frame()
        self.__control_frame = self.__control_frame_func()

    class __NetData:
        def __init__(self):
            self.host = 'Offline'
            self.port = 56789
            self.__get_host()

        def __get_host(self):
            temp = subprocess.run('arp -a', capture_output=True)
            for line in temp.stdout.decode('utf-8').split('\r'):
                if '90-4c-e5-c6-c4-89' in line:
                    self.host = line.strip().split(' ', 1)[0]

    def __connection_frame(self):
        frame = tkinter.Frame(master=self.__root)
        ip_entry = tkinter.Entry(master=frame, background='black', foreground='white',
                                 insertbackground='white', insertwidth=1, font=('calibri', 20, 'bold'),
                                 justify='center', width=15)
        ip_entry.insert(0, self.__net_data.host)
        ip_entry.focus()
        ip_entry.pack()

        error_label = tkinter.Label(master=frame, font=('calibri', 10, 'bold'),
                                    text='', foreground='red')
        connect_button = tkinter.Button(master=frame, text='Connect',
                                        font=('calibri', 10, 'bold'),
                                        command=lambda: self.__login(ip_entry.get(), error_label), padx=10,
                                        bg='black', fg='white', activebackground='gray')
        connect_button.pack(pady=5)

        return frame

    def __control_frame_func(self):
        frame = tkinter.Frame(master=self.__root)
        up_button = tkinter.Button(master=frame, text='Up', font=('calibri', 12),
                                   command=self.__up, padx=10, bg='black', fg='white',
                                   activebackground='gray', repeatdelay=500, repeatinterval=250)
        down_button = tkinter.Button(master=frame, text='Down', font=('calibri', 12),
                                     command=self.__down, padx=10, bg='black', fg='white',
                                     activebackground='gray')
        mute_button = tkinter.Button(master=frame, text='Mute', font=('calibri', 12),
                                     command=self.__mute, padx=10, bg='black', fg='white',
                                     activebackground='gray')
        kill_button = tkinter.Button(master=frame, text='Kill Zoom', font=('calibri', 12),
                                     command=self.__kill_zoom, padx=10, bg='black', fg='red',
                                     activebackground='gray')
        up_button.pack(fill='x')
        down_button.pack(fill='x')
        mute_button.pack(fill='x')
        kill_button.pack(fill='x')
        return frame

    def __controls(self):
        self.__connect_frame.forget()
        self.__control_frame.pack(expand=True, fill='both')

    def __login(self, ip, error_label):
        def show_error(error):
            error_label.config(text=f'Cant connect. {error}')
            error_label.pack()

        try:
            self.__connection.connect((ip, self.__net_data.port))
            self.__connection.send(b'ThisIsACode4334')
            data = self.__connection.recv(1024)
            if data == b'IN':
                self.__controls()
        except ConnectionRefusedError:
            show_error('Refused')
        except TimeoutError:
            show_error('Time out')
        except socket.gaierror:
            pass

    def __call__(self):
        self.__connect_frame.pack()
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
