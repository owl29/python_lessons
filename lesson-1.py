# coding: UTF-8
import sys
print("Hello, python!")
print("こんにちは")
print (sys.stdin.encoding)      #-> UTF-8
print (sys.stdout.encoding)     #-> UTF-8
print (sys.stderr.encoding)     #-> UTF-8
print ('One', 'Two', "Three")   #-> One Two Three
print ("Hello!", "Satou",)      #-> Hello! Satou
print (3.14e8)                  #-> 314000000.0
print (0x4F)                    #-> 79
print (3+4j)                    #-> (3+4j)

amari = 10 % 3

if amari != 0:
  print ("割り切れませんでした")
  print ("余りは",amari,"です")

#coding: UTF-8

print ("Start")
x = 0
y = 1

if x == 0:
  print ("x is 0")

  if y == 0:
    print ("y is 0")
  if y != 0:
    print ("y is not 0")
    print("YYYY")

print ("End")

list = ["A", "B", "C", "D", "E"]
print ("対象リスト", list)

print ("[1:2]  ", list[1:2])
print ("[1:-1] ", list[1:-1])
print ("[1:]   ", list[1:])
print ("[:2]   ", list[:2])
print ("[:]    ", list[:])
