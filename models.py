import typing

ROLE_TYPE = typing.Literal["roro_jonggrang", "bandung_bondowoso", "jin_pembangun", "jin_pengumpul"]

class User:
    def __init__(self, arr: tuple[str, str, ROLE_TYPE]) -> None:
        self.nama = arr[0]
        self.pwd = arr[1]
        self.role = arr[2]
        
class Candi:
    def __init__(self, arr: tuple[int, str, int, int, int]) -> None:
        self.id = arr[0]
        self.pembuat = arr[1]
        self.pasir = arr[2]
        self.batu = arr[3]
        self.air = arr[4]

class Bahan:
    def __init__(self, arr: tuple[str, str, int]):
        self.jenis = arr[0]
        self.deskripsi = arr[1]
        self.jumlah = arr[2]
        
class Command:
    def __init__(self, arr: tuple[str, str]) -> None:
        self.nama = arr[0]
        self.deskripsi = arr[1]

VALID_TYPE = typing.Union[Candi, User, Bahan, Command, int, str, list, None]
FILENAME = typing.Literal["bahan_bangunan.csv", "candi.csv", "user.csv"]
NMAX = 102

class Array:
    def __init__(self, arr : tuple[list[VALID_TYPE], int]) -> None:
        self.arr = arr[0]
        self.neff = arr[1]

BANDUNG_COMMANDS = Array((
    [
        Command(("summonjin", "Memanggil jin dari dunia lain")),
        Command(("hapusjin", "Menghilangkan jin")),
        Command(("ubahjin", "Mengubah tipe jin")),
        Command(("batchkumpul","Mengerahkan seluruh jin pengumpul untuk mengumpulkan bahan bangunan")),
        Command(("batchbangun","Mengerahkan seluruh jin pembangun untuk membangun candi")),
        Command(("laporanjin", "Mengambil laporan jin untuk mengetahui kinerja dari para jin")),
        Command(("laporancandi","Mengambil laporan candi untuk mengetahui progress pembangunan candi")),
        Command(("undo", "Mengembalikan jin yang telah dipecat")),
        Command(("logout", "Untuk keluar dari akun")),
        Command(("save", "Untuk menyimpan data program ke suatu folder")),
        Command(("exit", "Untuk keluar dari program dan kembali ke terminal"))
    ],
    11
))

RORO_COMMANDS = Array((
    [
        Command(("hancurkancandi", "Menghancurkan candi agar menggagalkan rencana Bandung Bondowoso")),
        Command(("ayamberkokok", "Menyelesaikan permainan dengan memalsukan pagi hari")),
        Command(("logout", "Untuk keluar dari akun")),
        Command(("save", "Untuk menyimpan data program ke suatu folder")),
        Command(("exit", "Untuk keluar dari program dan kembali ke terminal"))
    ],
    5
))

PEMBANGUN_COMMANDS = Array((
    [
        Command(("bangun", "Membangun candi dari bahan bangunan yang ada")),
        Command(("logout", "Untuk keluar dari akun")),
        Command(("save", "Untuk menyimpan data program ke suatu folder")),
        Command(("exit", "Untuk keluar dari program dan kembali ke terminal"))
    ],
    4
))
PENGUMPUL_COMMANDS = Array((
    [
        Command(("kumpul", "Mengumpulkan bahan-bahan yang diperlukan untuk membuat candi")),
        Command(("logout", "Untuk keluar dari akun")),
        Command(("save", "Untuk menyimpan data program ke suatu folder")),
        Command(("exit", "Untuk keluar dari program dan kembali ke terminal"))
    ],
    4
))

DEFAULT_COMMANDS = Array((
    [
        Command(("login", "Untuk masuk menggunakan akun")),
        Command(("save", "Untuk menyimpan data program ke suatu folder")),
        Command(("exit", "Untuk keluar dari program dan kembali ke terminal"))
    ],
    3
))