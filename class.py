class Teste():
    def __init__(self):
        self.bla = "bla"
    def test(self, tra):
        self.tra = tra

my_instance = Teste()
my_instance.test("Je")
print(my_instance.tra)
