import typing

ROLE_TYPE = typing.Literal["roro_jonggrang", "bandung_bondowoso", "jin_pembangun", "jin_pengumpul"]

class User:
    def __init__(self, arr: list[str, str, ROLE_TYPE]) -> None:
        self.nama = arr[0]
        self.pwd = arr[1]
        self.role = arr[2]
        
class Candi:
    def __init__(self, arr: list[int, str, int, int, int]) -> None:
        self.id = arr[0]
        self.pembuat = arr[1]
        self.pasir = arr[2]
        self.batu = arr[3]
        self.air = arr[4]

class Bahan:
    def __init__(self, arr: list[str,str,int]):
        self.jenis = arr[0]
        self.deskripsi = arr[1]
        self.jumlah = arr[2]
class Array:
    def __init__(self, arr : list[list[typing.Union[User, Candi]], int]) -> None:
        self.arr = arr[0]
        self.neff = arr[1]

VALID_TYPE = typing.Union[int, str, User, Candi, list]
FILENAME = typing.Literal["bahan_bangunan.csv", "candi.csv", "user.csv"]
NMAX = 102