import sys
import pandas as pd

def main():
    ods_file = pd.read_excel(sys.argv[1], engine="odf")
    
    print(ods_file.dtypes)
    print(ods_file)

if __name__ == "__main__":
    main()
