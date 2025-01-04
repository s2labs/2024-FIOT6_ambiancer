class Clock:
    nums = {0: "0xFF9867",
            1: "0xFF30CF",
            2: "0xFF18E7",
            3: "0xFF7A85",
            4: "0xFF10EF",
            5: "0xFF38C7",
            6: "0xFF5AA5",
            7: "0xFF42BD",
            8: "0xFF4AB5",
            9: "0xFF52AD"}

    def __init__(self,
                 ip_addr: int = "192.168.0.234",
                 user: str = "DVES_USER",
                 password: str = "****"):
        self.ip_addr = ip_addr
        self.user = user
        self.password = password

    def sendCode(self, code: str):
        print("sending code: {}".format(code))
        req_str_1 = 'http://{}/cm?user={}&password={}&cmnd=IRsend'.format(
            self.ip_addr,
            self.user,
            self.password)
        req_str_2 = '"Protocol":"NEC","Bits":32,"Data":{}'.format(code)
        req_str_2 = '{' + req_str_2 + '}'
        req_str = req_str_1 + req_str_2
        r = requests.get(req_str)
        print(r.text)

    def togglePower(self):
        self.sendCode('0xFFA25D')

    def number(self, num: int):
        self.sendCode(Clock.nums[num])

    def temp(self):
        self.sendCode('0xFF6897')

    def light(self):
        self.sendCode('0xFFB04F')

    def date(self):
        self.sendCode('0xFFE01F')

    def ok(self):
        self.sendCode('0xFFA857')

    def alarm(self):
        self.sendCode('0xFF906F')

    def left(self):
        self.sendCode('0xFF22DD')

    def right(self):
        self.sendCode('0xFFC23D')

    def set(self):
        self.sendCode('0xFF02FD')

    def func(self):
        self.sendCode('0xFF629D')

    def switch1224(self):
        self.sendCode('0xFFE21D')

    def onOff(self):
        self.sendCode('0xFFA25D')

    def sequence(self, seq: iter):
        for item in seq:
            item()
            # time.sleep(0.5)
            time.sleep(1.5)
            # self.sendCode("0xFFFFFF")

    def setTimer(self, m: int):
        assert (m <= 99 and m >= 0)
        digit1 = int(m/10)
        digit2 = m % 10
        print(digit1)
        print(digit2)
        self.sequence(
            (lambda: self.number(1),         # 1
             self.set,                    # SET
             lambda: self.number(digit1),  # num1
             lambda: self.number(digit2),  # num2
             self.ok)                     # OK
        )

    def pauseTimer(self):
        self.ok()

    def stopTimer(self):
        self.sequence(
            (self.ok,      # OK
             self.set,  # SET
             self.func)  # FUNC
        )
