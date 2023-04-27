import os, sys, math, time, argparse, datetime
import typing
from utils import *
from models import *

# F01 - Login
# Input: current user logged in, matriks user 
def login(user_var: typing.Optional[User], user_array: Array) -> typing.Optional[User]:
    if user_var == None:
        username = input("Username: ")
        password = input("Password: ")
        found = False
        
        for i in range(NMAX):
            if user_array.arr[i]:
                if user_array.arr[i].nama == username:
                    found = True
                    if user_array.arr[i].pwd == password:
                        print()
                        print(f"Selamat datang, {username}!")
                        print('Masukkan command "help" untuk daftar command yang dapat kamu panggil.')
                        return user_array.arr[i]
                    else:
                        print("Password salah!")
        if not found:
            print("Username tidak terdaftar!")
    else:
        print("Login gagal!")
        print(f'Anda telah login dengan username {user_var.nama}, silakan lakukan "logout" sebelum melakukan login kembali.')


# F13 - Load
# Input: nama folder, 
def load(path : str, users: list, candi : list, bahan_bangunan : list) -> None:
    folder_path = os.path.join(os.path.dirname(__file__), "save", path)
    if os.path.isdir(folder_path):
        print("Loading...")
        csv_parser(folder_path, "user.csv", users)
        csv_parser(folder_path, "candi.csv", candi)
        csv_parser(folder_path, "bahan_bangunan.csv", bahan_bangunan)
        print('Selamat datang di program "Manajerial Candi"')
        
    else:
        print(f'Folder "{path}" tidak ditemukan.')
        print()

# -----------------------=====================================----------------------------------

LOGGED_IN = None # Simpan user yang login

parser = argparse.ArgumentParser()
parser.add_argument("nama_folder", help="Folder berisi data csv", nargs='?', default=None)
args = parser.parse_args()

users = Array([[None for i in range(NMAX)], 0])
candi = Array([[None for i in range(NMAX)], 0])
bahan_bangunan = Array([[None for i in range(NMAX)], 0])

if __name__ == "__main__":
    if args.nama_folder:
        load(args.nama_folder, users, candi, bahan_bangunan)
        while True:
            cmd = input(">>> ")
            if cmd == "login":
                LOGGED_IN = login(LOGGED_IN, users)
            elif cmd == "debug":
                print(LOGGED_IN.nama)
    else:
        print("Tidak ada nama folder yang diberikan!")
        print()
        print("Usage: python main.py <nama_folder>")
        sys.exit()
        
