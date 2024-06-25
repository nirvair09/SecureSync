import os
import shutil
import zipfile
from Crypto.Cipher import AES
import hashlib


class BackupEngine:
    def backup_files(self,source,destination,compress=True,encrypt=False,password=None):
        if not os.path.exists(destination):
            os.makedirs(destination)

        for foldername,subfolders,filenames in os.walk(source):
            for filename in filenames:
                file_path= os.path.join(foldername,filename)
                dest_path= os.path.join(destination,os.path.relpath(file_path,source))


                if not os.path.exists(os.path.dirname(dest_path)):
                    os.makedirs(os.path.dirname(dest_path))

                shutil.copy2(file_path,dest_path)

        if compress:
            with zipfile.ZipFile(destination + '.zip', 'w', zipfile.ZIP_DEFLATED) as backup_zip:
                for foldername, subfolders, filenames in os.walk(destination):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        backup_zip.write(file_path, os.path.relpath(file_path, destination))
        
        if encrypt and password:
            self.encrypt_file(destination + '.zip', password)



    def encrypt_file(self,file_path,password):
        buffer_size=64*1024
        key=hashlib.sha256(password.encode()).digest()
        iv = os.urandom(16)
        encryptor= AES.new(key,AES.MODE_CBC,iv)

        file_size=os.path.getsize(file_path)

        with open(file_path,'rb') as infile:
            with open(file_path+'.enc','wb') as outfile:
                outfile.write(iv)
                while True:
                    chunck= infile.read(buffer_size)
                    if len(chunck) == 0:
                        break
                    elif len(chunck)% 16 != 0:
                        chunck+=b' '*(16-len(chunck)%16)

                    outfile.write(encryptor.encrypt(chunck))


        os.remove(file_path)                