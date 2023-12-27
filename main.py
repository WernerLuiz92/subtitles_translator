import sys
from subtitle_translator import ExtractorHandler
from subtitle_translator import TranslatorHandler

def main():
    result = ExtractorHandler.main()
    # If the result is a tuple, the subtitles have been extracted successfully and need to be translated
    if isinstance(result, tuple):
        TranslatorHandler.main(result[0], result[1])
    
    print("\n\nDone!")
    
if __name__ == "__main__":
    main()