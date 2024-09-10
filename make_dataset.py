import os
import wave
import shutil
import random

def get_wav_file_size(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        # 获取文件大小（以字节为单位）
        file_size = os.path.getsize(file_path)
        return file_size


def filter_file_by_size(source_directory_list, destination_directory, metadata, random_meta_data):
    for source_directory in source_directory_list:
        wav_files = [f for f in os.listdir(source_directory) if f.endswith('.wav')]

        min_size = 500
        speaker_name = source_directory.split('/')[-1]

        filtered_files = [f for f in wav_files if get_wav_file_size(os.path.join(source_directory, f)) / 1024 >= min_size]
        print(f"Found {len(filtered_files)} WAV files with size greater than or equal to {min_size} KB.")
        
        for f in filtered_files:
            source_file = os.path.join(source_directory, f)
            destination_file = os.path.join(destination_directory, f)
            shutil.copy(source_file, destination_file)
        
        with open(metadata, 'a+') as metadata_file:
            for file in filtered_files:
                text_file = file.replace('.wav', '.lab')
                if os.path.exists(os.path.join(source_directory, text_file)):
                    data_piece = str(file)
                    data_piece += f"|{speaker_name}|EN|"
                    with open(os.path.join(source_directory, text_file), "r") as text_file:
                        data_piece += text_file.read().strip()
                    metadata_file.write(data_piece + "\n")

    with open(metadata, "r") as metadata_file:
        dataset =[line for line in metadata_file]
    
    len(dataset)
    random.shuffle(dataset)
    with open(random_meta_data, "w") as metadata_file:
        metadata_file.writelines(dataset)

if __name__ == '__main__':
    directory = ["/data1/ziyiliu/datasets/tts/genshin/Leidian",
                 "/data1/ziyiliu/datasets/tts/genshin/Bachong",
                 "/data1/ziyiliu/datasets/tts/genshin/Naxida",
                 "/data1/ziyiliu/datasets/tts/genshin/Nawei",
                 "/data1/ziyiliu/datasets/tts/genshin/Wanye"]
    
    metadata = "/data1/ziyiliu/tts/Bert-VITS2/data/genshin/esd.list"
    random_metadata = "/data1/ziyiliu/tts/Bert-VITS2/data/genshin/random_esd.list"
    data_save_path = "/data1/ziyiliu/tts/Bert-VITS2/data/genshin/raw"
    filtered_files = filter_file_by_size(directory, data_save_path, metadata, random_metadata)