from aiogram.types import ContentType
from aiogram import F, types
from moviepy import VideoFileClip

from data.settings import bot, dp
import os


# Videoni dumaloq holatga o'girish
# @dp.message(F.video)
# async def test(message:types.Message):
#     height = message.video.height
#     width = message.video.width
#     file_id = message.video.file_id
#     filename = message.video.file_name
#     file_size = (message.video.file_size) / (1024*1024)
#     file_type = message.video.mime_type
#     duration = message.video.duration
#     if duration>60:
#         await message.answer("Iltimos 1 daqiqali video yuboring!")
#     else:
#         if file_size>10:
#             await message.answer("Iltimos video hajmi 10 MB gacha bo'lsin!")
#         else:
#             file = await bot.get_file(file_id=file_id)
#             import time
#             custom_file_name = f"{message.from_user.id}_{time.time()}.mp4"
#             await bot.download(file=file, destination=custom_file_name)
#             clip = VideoFileClip(filename=custom_file_name)
#             target_width = 640
#             target_height = 640
#             resize_video = clip.resize((target_height, target_width))
#             import time
#             custom_file_name2 = f"{message.from_user.id}_{time.time()}.mp4"
#             resize_video.write_videofile(custom_file_name2, codec='libx264')
#             sending_file = types.input_file.FSInputFile(path=custom_file_name2,filename=filename)
#             await bot.send_chat_action(action='upload_video_note',chat_id=message.chat.id)
#             await message.answer_video_note(video_note=sending_file)
#             try:
#                 if os.path.isfile(custom_file_name2):
#                     os.remove(custom_file_name2)
#                 if os.path.isfile(custom_file_name):
#                     os.remove(custom_file_name)
#             except:
#                 pass
# Videoni qo'shiq holatga o'girish
@dp.message(F.video)
async def test(message:types.Message):
    height = message.video.height
    width = message.video.width
    file_id = message.video.file_id
    filename = message.video.file_name
    file_size = (message.video.file_size) / (1024*1024)
    file_type = message.video.mime_type
    duration = message.video.duration
    if file_size>20:
        await message.answer("Iltimos video hajmi 20 MB gacha bo'lsin!")
    else:
        file = await bot.get_file(file_id=file_id)
        import time
        custom_file_name = f"{message.from_user.id}_{time.time()}.mp4"
        await bot.download(file=file, destination=custom_file_name)
        clip = VideoFileClip(filename=custom_file_name)
        import time
        audio = clip.audio
        custom_file_name2 = f"{message.from_user.id}_{time.time()}.mp3"
        audio.write_audiofile(custom_file_name2)
        clip.close()
        sending_file = types.input_file.FSInputFile(path=custom_file_name2,filename=filename)
        await bot.send_chat_action(action='upload_audio',chat_id=message.chat.id)
        await message.answer_audio(audio=sending_file)
        try:
            if os.path.isfile(custom_file_name2):
                os.remove(custom_file_name2)
            if os.path.isfile(custom_file_name):
                os.remove(custom_file_name)
        except Exception as e:
            print(e)