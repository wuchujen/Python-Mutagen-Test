from mutagen import File as mutagen_file
import os
import sqlite3

# mutagen_data = mutagen_file('Y:\\Music\\temp\\等一個人咖啡.m4a', None, True)
# title = mutagen_data['title'][0]
# album = mutagen_data['album'][0]
# artist = mutagen_data['artist'][0]
# albumartist = mutagen_data['albumartist'][0]
# date = mutagen_data['date'][0]
# genre = mutagen_data['genre'][0]
# tracknumber = mutagen_data['tracknumber'][0]
# discnumber = mutagen_data['discnumber'][0]
# length = mutagen_data.info.length

# %%
root_path = 'Y:\\Music\\Jazz'
db_filename = 'music.db'
db_file = os.path.join(os.getcwd(), db_filename) 

## Create Main Table is Database does not exist
if not os.path.exists(db_file):
      db_exists = False
else:
      db_exists = True

if not db_exists:
      conn = sqlite3.connect(db_file)
      with conn:
            conn.execute('''CREATE TABLE SONG_INFO
                  (TITLE           TEXT,
                  ALBUM            TEXT,
                  ARTIST           TEXT,
                  FILE             TEXT NOT NULL
                  );''')
            print('Table created successfully')
 

# %%
conn = sqlite3.connect(db_file)
with conn:
      c = conn.cursor()
      c.execute("SELECT FILE FROM SONG_INFO")
      db_file_list = c.fetchall()
      # for row in a:
      #       print(row)


file_list = []
for root, dirs, files in os.walk(root_path):
   for name in files:
      file_path = os.path.join(root, name)
      if name.endswith(('.mp3','.flac')) and not ((file_path ,) in db_file_list):
            mutagen_data = mutagen_file(file_path)
            file_list.append((mutagen_data['title'][0], mutagen_data['album'][0],
                  mutagen_data['artist'][0], file_path))
print('Number of new songs added:', len(file_list))

##   for name in dirs:
##     print(os.path.join(root, name))
# %%

## Create Main Table is Database does not exist
conn = sqlite3.connect(db_file)
with conn:
      conn.executemany('''INSERT INTO 
            SONG_INFO (TITLE, ALBUM, ARTIST, FILE) 
            VALUES (?, ?, ?, ?)''', file_list)

      conn.commit()
      print("Records created successfully")


# %%
