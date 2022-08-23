import os
from time import sleep



path = os.getcwd()
files = os.listdir(path)

#install package
os.system('sudo apt install calibre -y && sudo apt update')

#remove espacos e insere _
for file in files:
   os.rename(os.path.join(path, file), os.path.join(path, file.replace(' ', '_')))

for file in files:
    if file.endswith('.pdf'):
        f = file.split('.')
        f = f[0]
        os.system(f'ebook-convert {file} {f}.epub')

sleep(10)
print ('Finalizado.....')