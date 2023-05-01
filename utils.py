import typing, os, datetime
from collections.abc import Callable
from models import *

# Membuat seed awal berdasarkan epoch time
now = datetime.datetime.today()
seconds = now.timestamp()
seed = round(seconds)

def neg(a: int) -> int:
    # Mengembalikan negatif dari a
    return a * -1

def smallest_id(array_candi: Array, id = 1):
    for i in range(array_candi.neff):
        if array_candi.arr[i].id == id:
            return smallest_id(array_candi, id + 1)
    return id

def tambah_bahan(array_bahan: Array, tambahan: tuple[int,int,int]) -> Array:
    # Asumsi pasir index 0, batu index 1, air index 2
    array_bahan.arr[0].jumlah += tambahan[0]
    array_bahan.arr[1].jumlah += tambahan[1]
    array_bahan.arr[2].jumlah += tambahan[2]
    
    return array_bahan

def kurangi_bahan(array_bahan: Array, kurangan: tuple[int,int,int]) -> Array:
    # Asumsi pasir index 0, batu index 1, air index 2
    array_bahan.arr[0].jumlah -= kurangan[0]
    array_bahan.arr[1].jumlah -= kurangan[1]
    array_bahan.arr[2].jumlah -= kurangan[2]
    
    return array_bahan

def binary_question(text: str) -> str:
    # Mengulang pertanyaan sampai jawaban antara Y atau N kemudian mengembalikan jawaban tersebut
    choice = input(text).upper()
    if choice != "Y" and choice != "N":
        return binary_question(text)
    return choice

def search_nama(array: Array, nama: str) -> int:
    # Mencari nama dalam matriks user dan mengembalikan indexnya jika ditemukan
    for i in range(array.neff):
        if array.arr[i] == None:
            continue
        elif array.arr[i].nama == nama:
            return i
    return -1

def search_id(candi_array: Array, id: int) -> int:
    # Mencari nama dalam matriks user dan mengembalikan indexnya jika ditemukan
    for i in range(candi_array.neff):
        if candi_array.arr[i] == None:
            continue
        elif candi_array.arr[i].nama == id:
            return i
    return -1

def search_pembuat(array_candi: Array, nama_pembuat: str) -> int:
    # Mencari pembangun dalam matriks candi dan mengembalikan indexnya jika ditemukan
    for i in range(array_candi.neff):
        if array_candi.arr[i] == None:
            continue
        elif array_candi.arr[i].pembuat == nama_pembuat:
            return i
    return -1

def insert_empty(arr: Array, item: typing.Union[list, User, Candi], i = 0) -> Array:
    # Memasukkan item ke index array paling kecil yang kosong 
    if arr.arr[i] != None:
        return insert_empty(arr, item, i + 1)
    else:
        arr.arr[i] = item
        arr.neff += 1
        return arr

    
def find_empty(arr: Array, i = 0) -> int:
    # Mengembalikan index di array yang kosong
    if i >= NMAX:
        return -1
    elif arr.arr[i] != None:
        return find_empty(arr, i + 1)
    else:
        return i

def jin_sort(a: JinReport, b: JinReport) -> bool:
    # Mengembalikan True jika jumlah candi jin a lebih besar daripada b atau jumlah keduanya sama dan nama b lebih tinggi
    # Dengan fungsi bubble_sort, mengembalikan array yang berurut dari jin terajin hingga jin termalas dengan urutan leksikografis sesuai
    
    return a.jumlah > b.jumlah or (a.jumlah == b.jumlah and a.nama < b.nama)

def bubble_sort(arr: Array, comparator: Callable[[JinReport, JinReport], bool]) -> Array:
    # Mengembalikan array yang sudah di-sort sesuai fungsi comparator
    for i in range(arr.neff):
        for j in range(arr.neff):
            if comparator(arr.arr[i],arr.arr[j]):
                arr.arr[i],arr.arr[j] = arr.arr[j], arr.arr[i]
    return arr

def rmv(arr: Array, index: int, i: int = 0) -> Array:
    # Mengosongkan suatu index pada list
    if index == i:
        arr.arr[i] = None
        arr.neff -= 1
        return arr
    else:
        return rmv(arr, index, i + 1)

def pop(arr: Array, i: int) -> VALID_TYPE:
    # Mengembalikan index terakhir dari suatu array untuk stack, kombinasi dengan remove
    if arr.arr[i] != None:
        arr.arr[i] = arr.arr[i+1]
        return pop(arr,i+1)
    else:
        arr.neff -= 1
        return arr
    
def max(a: int, b: int) -> int:
    return a if a > b else b

def randomize(a: int, b : int) -> int:
    # Mengembalikan jumlah random dari range a sampai b menggunakan lcg
    global seed
    multiplier = 123813757
    increment = 102391847223
    modulus = 2**32
    
    res = seed = (multiplier*seed+increment) % modulus
    
    return res % (b + (1-a)) + a

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
                    
            tupled_item = tuple(item)
            
            if file == "bahan_bangunan.csv":
                arr.arr[arr.neff] = Bahan(tupled_item)
            elif file == "candi.csv":
                arr.arr[arr.neff] = Candi(tupled_item)
            else:
                arr.arr[arr.neff] = User(tupled_item)
            arr.neff += 1
            
            r = f.readline()
    return arr

# buat ngetes doang
def print_user(arr):
    for i in range(arr.neff):
        print(arr.arr[i].nama, arr.arr[i].pwd, arr.arr[i].role)