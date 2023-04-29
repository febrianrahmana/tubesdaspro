import typing, os
from collections.abc import Callable
from models import *
import random

# TODO: append/konso, head, tail

# Belum dipake
def not_in(arr: Array, item: VALID_TYPE) -> bool:
    # Mengembalikan True jika menemukan item dalam array
    for i in range(arr.neff):
        if arr.arr[i] == item:
            return True
    return False

def binary_question(text: str) -> str:
    # Mengulang pertanyaan sampai jawaban antara Y atau N kemudian mengembalikan jawaban tersebut
    choice = ""
    while choice != "Y" or choice != "N":
        choice = input(text).upper()
    return choice

def search_nama(user_array: Array, nama: str) -> int:
    # Mencari nama dalam matriks user dan mengembalikan indexnya jika ditemukan
    for i in range(user_array.neff):
        if user_array.arr[i].nama == nama:
            return i
    return -1

def search_id(candi_array: Array, id: int) -> int:
    # Mencari nama dalam matriks user dan mengembalikan indexnya jika ditemukan
    for i in range(candi_array.neff):
        if candi_array.arr[i].nama == id:
            return i
    return -1

# Belum dipake
def length(arr: list) -> int:
    # Mengembalikan jumlah index di list yang terisi
    total = NMAX
    for i in range(NMAX):
        if arr[i] == None:
            total -= 1
    return total

def insert_empty(arr: Array, item: typing.Union[list, User, Candi], i = 0) -> Array:
    # Memasukkan item ke index array paling kecil yang kosong 
    if arr.arr[i] != None:
        insert_empty(arr, item, i + 1)
    else:
        arr.arr[i] = item
        arr.neff += 1
        return arr

    
def find_empty(arr: Array, i = 0) -> int:
    # Mengembalikan index di array yang kosong
    if i >= NMAX:
        return -1
    elif arr.arr[i] != None:
        find_empty(arr, i + 1)
    else:
        return i

# TODO reimplement sort (probably use konso, head, tail concept to make it recursive)
def bigger(a: typing.Union[int, str], b: typing.Union[int, str]) -> typing.Union[int,str]:
    # Return bigger value for comparator
    return a if a > b else b

def bubble_sort(arr: list, comparator: Callable):
    pass

def rmv(arr: Array, index: int, i: int = 0) -> Array:
    # Mengosongkan suatu index pada list
    if index == i:
        arr.arr[i] = None
        arr.neff -= 1
        return arr
    else:
        return rmv(arr, index, i + 1)

def pop(arr: Array, i: int) -> Array:
    # Menghapus suatu index pada array dan menggeser index
    if arr.arr[i] != None:
        arr.arr[i] = arr.arr[i+1]
        return pop(arr,i+1)
    else:
        arr.neff -= 1
        return arr
    
# TODO implement lcg randomization
def randomize(a: int,b : int) -> int:
    # Mengembalikan jumlah random dari range a sampai b
    return random.randint(a,b)

def csv_writer(folder_path : str, users : Array, candi : Array, bahan_bangunan: Array) -> None:
    pass

def csv_parser(folder_path : str, file: FILENAME, arr: Array) -> None:
    # Membaca file csv kemudian mengembalikan sebagai array
    arr.neff = 0
    # Pembacaan file
    with open(os.path.join(folder_path,file), 'r') as f:
        # Menghitung jumlah kolom
        column_count = 1
        column = f.readline()
        for i in range(len(column)):
            if column[i] == ';':
                column_count += 1
        
        # Membaca file
        r = f.readline()
        # Repeat until
        while r:
            # Inisialisasi item kosong
            text = ""
            item = [None for i in range(column_count)]
            prop = 0
            
            # CSV parser
            for i in range(len(r)):
                if r[i] != ';' and r[i] != '\n':
                    text += r[i]
                else:
                    item[prop] = int(text) if text.isnumeric() else text
                    prop += 1
                    text = ""
            
            if file == "bahan_bangunan.csv":
                arr.arr[arr.neff] = Bahan(item)
            elif file == "candi.csv":
                arr.arr[arr.neff] = Candi(item)
            else:
                arr.arr[arr.neff] = User(item)
            arr.neff += 1
            
            r = f.readline()
    return arr