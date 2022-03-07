from color_wave_mapping import ColorWave
# from HueWaveApp import HueWave


if __name__ == "__main__":
    chord = ColorWave("sverige.jpg").process_mapping(print_detected_colors=True)
    print(chord)
