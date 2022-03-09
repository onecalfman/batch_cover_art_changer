from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import eyed3
import magic

audio = []
image = ""

def select_audio():
    global audio, file_name_label
    audio = filedialog.askopenfilenames(filetypes = [("mp3","*.mp3")])
    #audio = filedialog.askopenfilenames()
    if not len(audio):
        label_text = "Keine Datei ausgewählt"
    else:
        file_name = audio[0].split('\\')[-1]
        #file_name = audio[0].split('/')[-1]
        if len(audio) == 1:
            label_text = file_name[0:50]
        else:
            label_text = file_name[0:45] + ' und ' + str(len(audio) - 1) + ' weitere'

    file_name_label.destroy()
    file_name_label = Label(window, text=label_text , font = 30)
    file_name_label.grid(column=1, row=2, columnspan = 3)

def select_image():
    global image, image_preview_label
    preview_size = 450, 450
    image = filedialog.askopenfilename()
    try:
        image_preview = Image.open(image)
        image_preview.thumbnail(preview_size, Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image_preview)
        image_preview_label.destroy()
        image_preview_label = Label(window, image = render)
        image_preview_label.image_preview = render
        image_preview_label.grid(row = 1, column = 4, rowspan=10)
    except:
        image_preview_label.destroy()
        image_preview_label = Label(window, text="Kein Bild ausgewählt \n oder Format nicht unterstützt.", font = 20)
        image_preview_label.grid(row = 1, column = 4, rowspan=10)



def change_cover():
    global status_label
    successful_cover_changes = 0
    failed_changes = []
    status_label.destroy()
    if image:
        for entry in audio:
            print(entry)
            audiofile = eyed3.load(entry)
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(image)
            try:
                if (audiofile.tag == None):
                    audiofile.initTag()
                audiofile.tag.images.set(3, open(image,'rb').read(), mime_type)
                audiofile.tag.save()
                print('changed')
                successful_cover_changes += 1
            except:
                failed_changes.append(entry)
                continue
        status = str(successful_cover_changes) + '/' + str(len(audio)) + ' erfolgreich geändert'
        status_label = Label(window, text=status , font = 30)
        status_label.grid(column=1, row=4, columnspan = 3)
    else:
        for entry in audio:
            try:
                print(entry)
                audiofile = eyed3.load(entry)
                #frame_id = ['0x00', '0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07', '0x08', '0x09', '0x0A', '0x0B', '0x0C', '0x0D', '0x0E', '0x0F', '0x10', '0x11', '0x12', '0x13', '0x14', 'OTHER', 'ICON', 'OTHER_ICON', 'FRONT_COVER', 'BACK_COVER', 'LEAFLET', 'MEDIA', 'LEAD_ARTIST', 'ARTIST', 'CONDUCTOR', 'BAND', 'COMPOSER', 'LYRICIST', 'RECORDING_LOCATION', 'DURING_RECORDING', 'DURING_PERFORMANCE', 'VIDEO', 'BRIGHT_COLORED_FISH', 'ILLUSTRATION', 'BAND_LOGO', 'PUBLISHER_LOGO', 'MIN_TYPE', 'MAX_TYPE']
                audiofile.tag.images.remove('')
                audiofile.tag.save()
                print('changed')
                successful_cover_changes += 1
            except:
                failed_changes.append(entry)
                continue
        status = str(successful_cover_changes) + '/' + str(len(audio)) + ' erfolgreich geändert'
        status_label = Label(window, text=status , font = 30)
        status_label.grid(column=1, row=4, columnspan = 3)
    if len(failed_changes):
        faile_files_label = Label(window, text="gescheitert: " + str(failed_changes) , font = 30)
        faile_files_label.grid(column=1, row=5, columnspan = 3)




window = Tk()

window.title("Change MP3 Cover")

audio_button = Button(window, text="Audio", command=select_audio, height = 10, width = 20 , font = 20)
audio_button.grid(column=1, row=1)

image_button = Button(window, text="Bild", command=select_image, height = 10, width = 20, font = 20)
image_button.grid(column=3, row=1)

change_button = Button(window, text="Cover ändern", command=change_cover, height = 10, width = 40, font = '20')
change_button.grid(column=1, row=3, columnspan = 3)

file_name_label = Label(window, text="" , font = 30)
file_name_label.grid(column=1, row=2, columnspan = 3)
image_preview_label = Label(window)

status_label = Label(window, text="" , font = 30)
status_label.grid(column=1, row=4, columnspan = 3)

window.mainloop()

