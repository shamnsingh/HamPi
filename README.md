V
cal responsive HAM Radio interface

tests:
    
    # Execute tests to check if SDR is recognized and samples can be read.
    bash run_tests.sh

visualizations:

    # Displays spectrogram of data of being read.
    python -m lib.visualizations.sampleData
