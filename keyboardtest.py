import sys,tty,termios,time
class _Getch:       
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
    inkey = _Getch()
    while(1):
            k=inkey()
            if k!='':break
    print(f"you pressed {ord(k)}")
    time.sleep(1)

def main():
    while True:
        get()


if __name__=='__main__':
    main()