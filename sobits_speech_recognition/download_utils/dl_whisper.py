import whisper

def main(args=None):
    model = whisper.load_model("small")
    # tiny, base, small, medium, large, large-v2, large-v3, large-v3-turbo

    print("Model load finished\n")

if __name__ == '__main__':
    main()