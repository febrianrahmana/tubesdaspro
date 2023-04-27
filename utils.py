import typing, os
from models import *
from main import FILENAME
# TODO : length, insert_empty, pop (remove at index),

def length(arr: list) -> int:
    idx = 0
    while arr[idx] != None:
        idx += 1
    return idx

def merge_sort(arr):
    if length(arr) <= 1:
        return arr
    
    # Divide the array into two sub-arrays
    mid = length(arr) // 2
    left_arr = arr[:mid]
    right_arr = arr[mid:]
    
    # Recursively sort the two sub-arrays
    left_arr = merge_sort(left_arr)
    right_arr = merge_sort(right_arr)
    
    # Merge the two sorted sub-arrays
    sorted_arr = []
    i = j = 0
    while i < length(left_arr) and j < length(right_arr):
        if left_arr[i] <= right_arr[j]:
            sorted_arr.append(left_arr[i])
            i += 1
        else:
            sorted_arr.append(right_arr[j])
            j += 1
    sorted_arr += left_arr[i:]
    sorted_arr += right_arr[j:]
    
    return sorted_arr

def rmv(arr: list, index: int, i: int = 0) -> list:
    if index == i:
        arr[i] = None
        return arr
    else:
        return rmv(arr, index, i + 1)

def pop(arr, i):
    if arr[i] != None:
        arr[i] = arr[i+1]
        return pop(arr,i+1)
    else:
        return arr
    
def csv_parser(folder_path : str, file: FILENAME, arr: Array) -> None:
    arr.neff = 0
    # Pembacaan file
    with open(os.path.join(folder_path,file)) as f:
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
                arr.arr[arr.neff] = item
            elif file == "candi.csv":
                arr.arr[arr.neff] = Candi(item)
            else:
                arr.arr[arr.neff] = User(item)
            arr.neff += 1
            
            r = f.readline()