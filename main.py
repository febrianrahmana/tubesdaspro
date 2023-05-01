import os, sys, math, time, argparse, datetime
import typing
from utils import *
from models import *

# F01 - Login
# Input: current user logged in, matriks user 
def login(users: Array) -> None:
    global LOGGED_IN, ALLOWED_COMMANDS
    if LOGGED_IN.nama == None:
        username = input("Username: ")
        password = input("Password: ")
        
        found_index = search_nama(users, username)
        if found_index != -1:
            if users.arr[found_index].pwd == password:
                print()
                print(f"Selamat datang, {username}!")
                print('Masukkan command "help" untuk daftar command yang dapat kamu panggil.')
                LOGGED_IN = users.arr[found_index]
                if LOGGED_IN.role == "bandung_bondowoso":
                    ALLOWED_COMMANDS = BANDUNG_COMMANDS
                elif LOGGED_IN.role == "roro_jonggrang":
                    ALLOWED_COMMANDS = RORO_COMMANDS
                elif LOGGED_IN.role == "jin_pembangun":
                    ALLOWED_COMMANDS = PEMBANGUN_COMMANDS
                else:
                    ALLOWED_COMMANDS = PENGUMPUL_COMMANDS
            else:
                print("Password salah!")
        else:
            print("Username tidak terdaftar!")
    else:
        print("Login gagal!")
        print(f'Anda telah login dengan username {LOGGED_IN.nama}, silakan lakukan "logout" sebelum melakukan login kembali.')

# F02 - Logout
# Input: current user logged in
def logout() -> None:
    global LOGGED_IN
    if LOGGED_IN.nama != None:
        LOGGED_IN = User((None, None, None))
    else:
        print("Logout gagal!")
        print("Anda belum login, silakan login terlebih dahulu sebelum melakukan logout")
        
# F03 - Summon Jin
# Input: matriks user
def summonjin(logged_in: User) -> None:
    global users
    if logged_in.role != "bandung_bondowoso":
        print("Summon jin hanya dapat diakses oleh akun Bandung Bondowoso.")
        return
    if users.neff < 102:
        print("""Jenis jin yang dapat dipanggil:
            (1) Pengumpul - Bertugas mengumpulkan bahan bangunan
            (2) Pembangun - Bertugas membangun candi
        """)
        jenis_jin = ""
        while jenis_jin != "1" and jenis_jin != "2":
            print()
            jenis_jin = input("Masukkan nomor jenis jin ingin dipanggil: ")
            if jenis_jin != "1" and jenis_jin != "2":
                print()
                print(f'Tidak ada jenis jin bernomor "{jenis_jin}"!')
        if jenis_jin == "1":
            print()
            print('Memilih jin "Pengumpul"')
            jenis_jin = "jin_pengumpul"
        else:
            print()
            print('Memilih jin "Pembangun"')
            jenis_jin = "jin_pembangun"
        print()
        username = input("Masukkan username jin: ")
        while search_nama(users, username) != -1:
            print(f'\nUsername "{username}" sudah diambil!\n')
            username = input("Masukkan username jin: ")
                
        valid = False
        while not valid:
            password = input("Masukkan password jin: ")
            if len(password) < 5 or len(password) > 25:
                print("\nPassword panjangnya harus 5-25 karakter!\n")
            else:
                valid = True
        
        print("\nMengumpulkan sesajen...")
        print("Menyerahkan sesajen...")
        print("Membacakan mantra...")
        
        jin_baru = User((username, password, jenis_jin))
        insert_empty(users, jin_baru)
        
        print()
        print(f"Jin {username} berhasil dipanggil!")
    else:
        print("Jumlah Jin telah maksimal! (100 jin). Bandung tidak dapat men-summon lebih dari itu")

# F04 - Hilangkan Jin
# Input: matriks user
def hapusjin(logged_in: User) -> None:
    global users
    if logged_in.role != "bandung_bondowoso":
        print("Menghilangkan jin hanya dapat diakses oleh akun Bandung Bondowoso.")
        return
    username = input("Masukkan username jin: ")
    found_index = search_nama(users, username)
    
    if found_index != -1:
        choice = binary_question(f"Apakah anda yakin ingin menghapus jin dengan username {username} (Y/N)? ")
        if choice == "Y":
            print("\nJin telah berhasil dihapus dari alam gaib.")
            # TODO add removing mechanism, remember to remove candi made by said jin (to implement undo, save jin+candi to an array, make a model for it?)
    else:
        print("\nTidak ada jin dengan username tersebut.")
            
# F05 - Ubah Tipe Jin
# Input: users
def ubahjin(logged_in: User) -> None:
    global users
    if logged_in.role != "bandung_bondowoso":
        print("Ubah tipe jin hanya dapat diakses oleh akun Bandung Bondowoso.")
        return
    username = input("Masukkan username jin: ")
    found_index = search_nama(users, username)
    
    if found_index != -1 and users.arr[found_index].role != "bandung_bondowoso" and users.arr[found_index].role != "roro_jonggrang":
        if users.arr[found_index].role == "jin_pembangun":
            choice = binary_question('Jin ini bertipe "Pembangun". Yakin ingin mengubah ke tipe "Pengumpul" (Y/N)? ')
            if choice == "Y":
                users.arr[found_index].role = "jin_pengumpul"
                print("\nJin telah berhasil diubah.")
        else:
            choice = binary_question('Jin ini bertipe "Pengumpul". Yakin ingin mengubah ke tipe "Pembangun" (Y/N)? ')
            if choice == "Y":
                users.arr[found_index].role = "jin_pembangun"
                print("\nJin telah berhasil diubah.")
    else:
        print("\nTidak ada jin dengan username tersebut.")
        
# F06 - Jin Pembangun
# Input: logged in user, 
def bangun(logged_in: User) -> None:
    global bahan_bangunan, candi
    if logged_in.role != "jin_pembangun":
        print("Bangun candi hanya dapat diakses oleh akun Jin Pembangun.")
        return
    
    random_bahan = (randomize(0,5),randomize(0,5),randomize(0,5))
    
    if bahan_bangunan.arr[0].jumlah - random_bahan[0] >= 0 and bahan_bangunan.arr[1].jumlah - random_bahan[1] >= 0 and bahan_bangunan.arr[2].jumlah - random_bahan[2] >= 0:
        found_index = find_empty(candi)
        if found_index != -1:
            candi = insert_empty(candi, Candi((found_index, logged_in.nama, random_bahan[0], random_bahan[1], random_bahan[2])))
        bahan_bangunan = kurangi_bahan(bahan_bangunan, random_bahan)
        print("Candi berhasil dibangun.")
        print(f"Sisa candi yang perlu dibangun: {max(100-candi.neff,0)}")
    else:
        print("Bahan bangunan tidak mencukupi.")
        print("Candi tidak bisa dibangun!")
        

# F07 - Jin Pengumpul
# Input: logged in user
def kumpul(logged_in: User) -> None:
    global bahan_bangunan
    if logged_in.role != "jin_pengumpul":
        print("Kumpul hanya dapat diakses oleh akun Jin Pengumpul.")
        return
    
    random_bahan = (randomize(0,5),randomize(0,5),randomize(0,5))
    bahan_bangunan = tambah_bahan(bahan_bangunan, random_bahan)
    print(f"Jin menemukan {random_bahan[0]} pasir, {random_bahan[1]} batu, {random_bahan[2]} air.")

# F08 - Batch Bangun/Kumpul
# Input: logged in user
def batchkumpul(logged_in: User, user_array: Array) -> None:
    global bahan_bangunan
    if logged_in.role != "bandung_bondowoso":
        print("Batch kumpul hanya dapat diakses oleh akun Bandung Bondowoso.")
        return
    
    total_pengumpul = 0
    for i in range(user_array.neff):
        if user_array.arr[i].role == "jin_pengumpul":
            total_pengumpul += 1
            
    random_pasir = 0
    random_batu = 0
    random_air = 0
    
    if total_pengumpul != 0:
        for _ in range(total_pengumpul):
            random_pasir += randomize(0,5)
            random_batu += randomize(0,5)
            random_air += randomize(0,5)
        
        bahan_bangunan = tambah_bahan(bahan_bangunan, (random_pasir, random_batu, random_air))
        print(f"Mengerahkan {total_pengumpul} jin untuk mengumpulkan bahan")
        print(f"Jin menemukan total {random_pasir} pasir, {random_batu} batu, dan {random_air} air.")
        
    else:
        print("Kumpul gagal. Anda tidak punya jin pengumpul. Silakan summon terlebih dahulu.")    

def batchbangun(logged_in: User, user_array: Array) -> None:
    global candi
    if logged_in.role != "bandung_bondowoso":
        print("Batch bangun hanya dapat diakses oleh akun Bandung Bondowoso.")
        return
    
    array_pembangun = Array(([None for i in range(NMAX)],0))
    for i in range(user_array.neff):
        if user_array.arr[i].role == "jin_pembangun":
            array_pembangun = insert_empty(array_pembangun, user_array[i])
    
    array_candi = Array(([None for i in range(NMAX)], 0))
    
    if array_pembangun.neff != 0:
        for i in range(array_pembangun.neff):
            candi_buatan = Candi((array_candi.neff+1, array_pembangun.arr[i].nama, randomize(1,5), randomize(1,5), randomize(1,5)))
            array_candi = insert_empty(array_candi, candi_buatan)
        
        total_random_pasir = 0
        total_random_batu = 0
        total_random_air = 0
        for i in range(array_candi.neff):
            total_random_pasir += array_candi.arr[i].pasir
            total_random_batu += array_candi.arr[i].batu
            total_random_air += array_candi.arr[i].air
            
        bahan_terpakai = (total_random_pasir, total_random_batu, total_random_air)
        hasil_kurang_bahan = (bahan_bangunan.arr[0].jumlah - bahan_terpakai[0], bahan_bangunan.arr[1].jumlah - bahan_terpakai[1], bahan_bangunan.arr[2].jumlah - bahan_terpakai[2])
        
        print(f"Mengerahkan {array_pembangun.neff} jin untuk membangun candi dengan total bahan {total_random_pasir} pasir, {total_random_batu} batu, dan {total_random_air} air.")
        
        if hasil_kurang_bahan[0] >= 0 and hasil_kurang_bahan[1] >= 0 and hasil_kurang_bahan[2] >= 0:
            bahan_bangunan = kurangi_bahan(bahan_bangunan, bahan_terpakai)
            for i in range(array_candi.neff):
                candi = insert_empty(candi, array_candi.arr[i])
            print(f"Jin berhasil membangun total {array_candi.neff} candi.")
        else:
            print(f"Bangun gagal. Kurang {max(neg(hasil_kurang_bahan[0]),0)} pasir, {max(neg(hasil_kurang_bahan[1]),0)} batu, dan {max(neg(hasil_kurang_bahan[2]),0)} air.")
    else:
        print("Bangun gagal. Anda tidak punya jin pembangun. Silakan summon terlebih dahulu.")
        
    

# F09 - Laporan Jin
# Input: matriks jin, matriks candi, matriks bahan bangunan
def laporanjin(users: Array, candi: Array, bahan_bangunan: Array, logged_in: User) -> None:
    laporan_jin = Array(([None for i in range(NMAX)], 0))
    total_pengumpul = 0
    if logged_in.role != "bandung_bondowoso":
        print("Laporan jin hanya dapat diakses oleh akun Bandung Bondowoso.")
        return
    for i in range(candi.neff):
        found_index = search_nama(laporan_jin, candi.arr[i].pembuat)
        if found_index != -1:
            laporan_jin.arr[found_index].jumlah += 1
        else:
            laporan_jin = insert_empty(laporan_jin, JinReport((candi.arr[i].pembuat, 1)))
    
    for i in range(users.neff):
        if users.arr[i].role == "jin_pembangun" and search_nama(laporan_jin, users.arr[i].nama) == -1:
            laporan_jin = insert_empty(laporan_jin, JinReport((users.arr[i].nama, 0)))
        elif users.arr[i].role == "jin_pengumpul":
            total_pengumpul += 1
            
    laporan_jin = bubble_sort(laporan_jin, jin_sort)
    
    print(f"> Total Jin: {laporan_jin.neff+total_pengumpul}")
    print(f"> Total Jin Pengumpul: {total_pengumpul}")
    print(f"> Total Jin Pembangun: {laporan_jin.neff}")
    
    if laporan_jin.neff == 0:
        print(f"> Jin Terajin: -")
        print(f"> Jin Termalas: -")
    else:
        print(f"> Jin Terajin: {laporan_jin.arr[0].nama}")
        print(f"> Jin Termalas: {laporan_jin.arr[laporan_jin.neff-1].nama}")
    
    # Asumsi pasir di index 0, batu di index 1, air di index 2
    print(f"> Jumlah Pasir: {bahan_bangunan.arr[0].jumlah} unit")
    print(f"> Jumlah Air: {bahan_bangunan.arr[2].jumlah} unit")
    print(f"> Jumlah Batu: {bahan_bangunan.arr[1].jumlah} unit")

# F10 - Laporan Candi
# Input: matriks candi
def laporancandi(candi: Array, logged_in: User) -> None:
    if logged_in.role != "bandung_bondowoso":
        print("Laporan candi hanya dapat diakses oleh akun Bandung Bondowoso.")
        return
    
    def harga_candi(candi: Candi):
        return 10_000 * candi.pasir + 15_000 * candi.batu + 7_500 * candi.air
    
    def formatting(angka):
        terpisah_koma = "{:,}".format(angka)
        terpisah_titik = ""
        for i in range(len(terpisah_koma)):
            if terpisah_koma[i] == ",":
                terpisah_titik += "."
            else:
                terpisah_titik += terpisah_koma[i]
        return terpisah_titik
    
    candi_termahal = Candi((None,None,0,0,0))
    candi_termurah = Candi((None,None,0,0,0))
    
    if candi.neff > 0:
        total_pasir = 0
        total_batu = 0
        total_air = 0
        
        for i in range(candi.neff):
            total_pasir += candi.arr[i].pasir
            total_batu += candi.arr[i].batu
            total_air += candi.arr[i].air
            if harga_candi(candi.arr[i]) > harga_candi(candi_termahal):
                candi_termahal = candi.arr[i]
            elif harga_candi(candi.arr[i]) < harga_candi(candi_termurah):
                candi_termurah = candi.arr[i]
                
        print(f"> Total Candi: {candi.neff}")
        print(f"> Total Pasir yang digunakan: {total_pasir}")
        print(f"> Total Batu yang digunakan: {total_batu}")
        print(f"> Total Air yang digunakan: {total_air}")
        print(f"> ID Candi Termahal: {candi_termahal.id} (Rp {formatting(harga_candi(candi_termahal))})")
        print(f"> ID Candi Termurah: {candi_termurah.id} (Rp {formatting(harga_candi(candi_termahal))})")
    else:
        print("> Total Candi: 0")
        print("> Total Pasir yang digunakan: 0")
        print("> Total Batu yang digunakan: 0")
        print("> Total Air yang digunakan: 0")
        print("> ID Candi Termahal: -")
        print("> ID Candi Termurah: -")

# F11 - Hancurkan Candi
# Input: matriks candi
def hancurkancandi(logged_in: User) -> None:
    global candi
    if logged_in.role != "roro_jonggrang":
        print("Hancurkan candi hanya dapat diakses oleh akun Roro Jonggrang.")
        return
    id_candi = int(input("Masukkan ID candi: "))
    found_index = search_id(candi, id_candi)
    
    if found_index != -1:
        choice = binary_question(f"Apakah Anda yakin ingin menghancurkan candi ID: {id_candi} (Y/N)? ")
        if choice == "Y":
            candi = rmv(candi, found_index)
            print("\nCandi telah berhasil dihancurkan.")
    else:
        print("\nTidak ada candi dengan ID tersebut.")

# F12 - Ayam Berkokok
# Input: matriks candi
def ayamberkokok(logged_in: User) -> None:
    global candi
    if logged_in.role != "roro_jonggrang":
        print("Ayam berkokok hanya dapat diakses oleh akun Roro Jonggrang.")
        return
    print("Kukuruyuk.. Kukuruyuk..")
    print(f"\nJumlah Candi: {candi.neff}\n")
    if candi.neff < 100:
        print("Selamat, Roro Jonggrang memenangkan permainan!\n")
        print("*Bandung Bondowoso angry noise*")
        print("Roro Jonggrang dikutuk menjadi candi.")
        sys.exit()
    else:
        print("Yah, Bandung Bondowoso memenangkan permainan!")
        sys.exit()
    

# F13 - Load
# Input: nama folder, 
def load(path : str) -> None:
    global users, candi, bahan_bangunan
    folder_path = os.path.join(os.path.dirname(__file__), "save", path)
    if os.path.isdir(folder_path):
        print("Loading...")
        users = csv_parser(folder_path, "user.csv", users)
        candi = csv_parser(folder_path, "candi.csv", candi)
        bahan_bangunan = csv_parser(folder_path, "bahan_bangunan.csv", bahan_bangunan)
        print('Selamat datang di program "Manajerial Candi"')
        
    else:
        print(f'Folder "{path}" tidak ditemukan.')
        sys.exit()

# F14 - Save
# Input: logged in user
def save() -> None:
    global users, candi, bahan_bangunan
    print()
    folder = input("Masukkan nama folder: ")
    folder_path = os.path.join(os.path.dirname(__file__), "save", folder)
    print("\nSaving...")
    if not os.path.isdir(folder_path):
        print(f"\nMembuat folder save/{folder}")
        os.mkdir(folder_path)
    csv_writer(folder_path, users, candi, bahan_bangunan)
    print(f"\nBerhasil menyimpan data di folder save/{folder}!")

# F15 - Help
# Input: logged in user
def help(commands : Array) -> None:
    print("=========== HELP ===========")
    for i in range(commands.neff):
        print(f"{i+1}. {commands.arr[i].nama}")
        print(f"    {commands.arr[i].deskripsi}")

# F16 - Exit
# Input: logged in user
def exit() -> None:
    choice = binary_question("Apakah Anda mau melakukan penyimpanan file yang sudah diubah (Y/N)? ")
    if choice == "Y":
        save()
    sys.exit()
    
# B04 - Undo
# Input: jin purg, candi purg
def undo() -> None:
    global jin_purgatory, candi_purgatory
    pass
# -----------------------=====================================----------------------------------

# Variabel berisi akun yang sedang login dan commandsnya
LOGGED_IN = User((None, None, None)) # Simpan user yang login
ALLOWED_COMMANDS = DEFAULT_COMMANDS

# Parser untuk input nama folder
parser = argparse.ArgumentParser()
parser.add_argument("nama_folder", help="Folder berisi data csv", nargs='?', default=None)
args = parser.parse_args()

# Array data user, candi, dan bahan bangunan
users = Array(([None for i in range(NMAX)], 0))
candi = Array(([None for i in range(NMAX)], 0))
bahan_bangunan = Array(([None for i in range(NMAX)], 0))

# Array jin dan candi yang telah dihapus
jin_purgatory = Array(([None for i in range(NMAX)], 0))
candi_purgatory = Array(([None for i in range(NMAX)], 0))

# Run ketika file di call
if __name__ == "__main__":
    if args.nama_folder:
        # Load file csv
        load(args.nama_folder)
        # Main loop command
        while True:
            cmd = input(">>> ")
            if cmd == "login":
                login(users)
            elif cmd == "logout":
                logout()
            elif cmd == "summonjin":
                summonjin(LOGGED_IN)
            elif cmd == "hapusjin":
                hapusjin()
            elif cmd == "laporancandi":
                laporancandi(candi)
            elif cmd == "help":
                help(ALLOWED_COMMANDS)
            elif cmd == "debug":
                print_user(users)
    else:
        print("Tidak ada nama folder yang diberikan!")
        print()
        print("Usage: python main.py <nama_folder>")
        sys.exit()
        
