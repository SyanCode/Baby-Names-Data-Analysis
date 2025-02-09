import pandas as pd
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('prenoms_processing.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_csv_file(filename, sep=";", encoding="utf-8"):
    """
    Safely load a CSV file with error handling
    
    Args:
        filename (str): Path to the CSV file
        sep (str, optional): CSV separator. Defaults to ";".
        encoding (str, optional): File encoding. Defaults to "utf-8".
    
    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist")
        
        # Debugging: read raw file contents
        with open(filename, 'r', encoding=encoding) as f:
            first_line = f.readline().strip()
            logging.info(f"Raw first line: {first_line}")
        
        # Try multiple parsing strategies
        try:
            # Strategy 1: Explicit separator
            df = pd.read_csv(filename, sep=',', encoding=encoding)
        except Exception as e:
            logging.error(f"First parsing attempt failed: {e}")
            try:
                # Strategy 2: Python engine with explicit separator
                df = pd.read_csv(filename, sep=',', encoding=encoding, engine='python')
            except Exception as e:
                logging.error(f"Second parsing attempt failed: {e}")
                raise
        
        # Detailed logging of file contents
        logging.info(f"File: {filename}")
        logging.info(f"Total rows: {len(df)}")
        logging.info(f"Columns found: {list(df.columns)}")
        
        # Validate required columns and rename them to match our processing
        required_columns = {
            'sexe': 'Sexe', 
            'prenom': 'Prenom', 
            'nombre': 'Nombre'
        }
        
        # Detailed check for missing columns
        missing_columns = []
        for col in required_columns.keys():
            if col not in df.columns:
                missing_columns.append(col)
                logging.error(f"Column '{col}' is missing")
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Rename columns to match our processing
        df = df.rename(columns=required_columns)
        
        # Convert 'Sexe' to string and map numeric values to 'M' and 'F'
        df['Sexe'] = df['Sexe'].map({1: 'M', 2: 'F'})
        
        logging.info(f"Successfully loaded {filename}")
        return df
    
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        logging.error(f"No data in {filename}")
        sys.exit(1)
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing {filename}: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error loading {filename}: {e}")
        sys.exit(1)

def process_top_names(df, year, top_n=10):
    """
    Process and log top names for a given year
    
    Args:
        df (pd.DataFrame): Input DataFrame
        year (int): Year of the data
        top_n (int, optional): Number of top names to display. Defaults to 10.
    """
    try:
        top_names = df.groupby("Prenom")["Nombre"].sum().nlargest(top_n)
        
        logging.info(f"\nTop {top_n} prénoms en {year} :")
        for i, (prenom, occurrence) in enumerate(top_names.items(), 1):
            print(f"Prénom {year} n°{i} = {prenom} - Occurrence = {occurrence}")
        
        return top_names
    except Exception as e:
        logging.error(f"Error processing top names for {year}: {e}")
        return pd.Series()

def main():
    try:
        # Load CSV files
        prenoms2003 = load_csv_file("Prenoms2003.csv")
        prenoms2004 = load_csv_file("Prenoms2004.csv")

        # Process and merge data
        prenoms_2003_2004 = pd.concat([prenoms2003, prenoms2004], ignore_index=True)

        # Export merged data
        try:
            prenoms_2003_2004.to_csv("Prenoms2003-2004.csv", sep=";", encoding="utf-8", index=False)
            logging.info("Successfully exported merged data to Prenoms2003-2004.csv")
        except PermissionError:
            logging.error("Permission denied when writing Prenoms2003-2004.csv")
        except Exception as e:
            logging.error(f"Error exporting merged data: {e}")

        # Process top names
        process_top_names(prenoms2003, 2003)
        process_top_names(prenoms2004, 2004)

        # Process top names by gender
        try:
            filles = prenoms_2003_2004[prenoms_2003_2004["Sexe"] == "F"].groupby("Prenom")["Nombre"].sum().nlargest(10)
            garcons = prenoms_2003_2004[prenoms_2003_2004["Sexe"] == "M"].groupby("Prenom")["Nombre"].sum().nlargest(10)

            logging.info("\nTop 10 prénoms filles en 2003-2004 :")
            for i, (prenom, occurrence) in enumerate(filles.items(), 1):
                print(f"Prénom Fille n°{i} = {prenom} - Occurrence = {occurrence}")

            logging.info("\nTop 10 prénoms garçons en 2003-2004 :")
            for i, (prenom, occurrence) in enumerate(garcons.items(), 1):
                print(f"Prénom Garçon n°{i} = {prenom} - Occurrence = {occurrence}")
        
        except Exception as e:
            logging.error(f"Error processing names by gender: {e}")

        # Export grouped data
        try:
            prenoms_2003_2004_grouped = prenoms_2003_2004.groupby("Prenom")["Nombre"].sum().reset_index()
            prenoms_2003_2004_grouped.to_csv("Prenoms2003-2004_Jointure.csv", sep=";", encoding="utf-8", index=False)
            logging.info("Successfully exported grouped data to Prenoms2003-2004_Jointure.csv")
        except PermissionError:
            logging.error("Permission denied when writing Prenoms2003-2004_Jointure.csv")
        except Exception as e:
            logging.error(f"Error exporting grouped data: {e}")

    except Exception as e:
        logging.error(f"Unexpected error in main processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()