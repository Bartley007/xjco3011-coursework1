from data_loader import init_database, load_sample_data

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    print("Loading sample data...")
    load_sample_data()
    print("Done!")
