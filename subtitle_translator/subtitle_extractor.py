# A simple CLI tool to extract subtitles from a video file using ffmpeg
import os
import re
import subprocess

# TODO: Add function to list all available languages
# TODO: Add function to extract subtitles from a selected language
# TODO: Add function to list all available files in a directory

class ExtractorHandler:
    @classmethod
    def main(cls, directory = "./media/"):
        print("This is a simple CLI tool to extract subtitles from a video file using ffmpeg.")
        print("Found the following files:")
        
        file_selected = cls.listMediaFiles(directory)
        
        if file_selected is None:
            return
        
        channel_to_extract = cls.listSubtitleChannels(file_selected, directory)
        
        if channel_to_extract is None:
            return
        
        print(channel_to_extract)
        print(file_selected)
        
        # If exists a file named {file_name}.srt, ask if the user wants to overwrite it
        if os.path.exists(directory + os.path.splitext(file_selected)[0] + ".srt"):
            print("File already exists. Do you want to overwrite it?")
            print("1. Yes")
            print("2. No")
            
            option = input("Select an option: ")
            
            if option is None or option == "" or int(option) < 1 or int(option) > 2:
                print("Invalid option.")
                return

            if int(option) == 1:
                os.remove(directory + os.path.splitext(file_selected)[0] + ".srt")
                print("File will be overwritten.")
            else:
                print("File will not be overwritten. Exiting...")
                return
        
        result = cls.extractSubtitles(file_selected, channel_to_extract, directory)
        
        if result is None or not result:
            return
        
        print("Subtitles extracted successfully! Do you want to translate the subtitles?")
        print("1. Yes")
        print("2. No")
        
        option = input("Select an option: ")
        
        if option is None or option == "" or int(option) < 1 or int(option) > 2:
            print("Invalid option.")
            return
        
        if int(option) == 1:
            return (file_selected, os.path.splitext(file_selected)[0] + ".srt")

    @classmethod
    def listMediaFiles(cls, directory):
        # List all files present in ./media
        files = os.listdir(directory)
        # Order the files alphabetically
        files.sort()
        
        
        # If the file is a subtitle file, remove it from the list
        files = [file for file in files if not file.endswith(".srt")]
        
        filesList = []
        
        if len(files) == 0:
            print("No files found.")
            return
        
        for idx, file in enumerate(files):
            print(f"\t - {idx+1}. {file}")
            filesList.append([idx+1, file])
        
        option = input("Select a file by its index: ")
        
        if option is None or option == "" or int(option) < 1 or int(option) > len(files):
            print("Invalid option.")
            return

        # Ask the user to select a file from the list by its index
        selectedFile = filesList[int(option) - 1]
        
        if selectedFile is None:
            return
        
        print(f"You selected {selectedFile[1]}")
        
        return selectedFile[1]

    @classmethod
    def listSubtitleChannels(cls, file, directory):
        command = f"ffmpeg -i {directory}{file}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        pattern = re.compile(r'Stream #\d+:\d+\(\w+\): Subtitle:')
        matches = re.findall(pattern, result.stderr)
        
        subtitle_channels = []
        
        if len(matches) == 0:
            print("No subtitle channels found.")
            return

        print("\nSubtitle channels found:")
        for match in matches:
            channel_info = match[match.find("Stream #")+8:match.find("(")].strip()
            language_code = match.split("(")[1].split(")")[0].strip()  # Extrai o código de idioma
            subtitle_channels.append((channel_info, language_code))

        print(f"\nWhat channel do you want to extract subtitles from?\n")
        for idx, channel in enumerate(subtitle_channels):
            print(f"\t {idx+1}. Channel: {channel[0]} Language: ({channel[1]})")

        option = input("Select a channel by its index: ")
        
        if option is None or option == "" or int(option) < 1 or int(option) > len(subtitle_channels):
            print("Invalid option.")
            return

        selected_channel = subtitle_channels[int(option) - 1]
        
        print(f"You selected the following channel: {selected_channel[0]} that corresponds to language ({selected_channel[1]})")
        
        return selected_channel
    
    @classmethod
    def extractSubtitles(cls, file, channel, directory):
        # Get the name of the file without the extension (e.g. file.move_in.mp4 -> file.move_in)
        file_name = os.path.splitext(file)[0]
        
        print(f"Extracting subtitles from {file_name} using channel {channel[0]}")

        # ffmpeg -i {directory}{file} -vn -an -map {channel[0]} -f srt {directory}{file_name}.srt
        command = f"ffmpeg -i {directory}{file} -vn -an -map {channel[0]} -f srt {directory}{file_name}.srt"
        
        # Run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(result.stderr)
            return False

        print(f"Subtitles extracted successfully to {file_name}.srt")
        
        return True