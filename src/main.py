from src.backend.metadata_handler import MetadataHandler

if __name__ == "__main__":
    print("Hallo")

    save = MetadataHandler()

    save.save_stations()
    save.save_train_categories()
    save.save_train_types()

    print(save.load_station_dict())
    print(save.load_train_category_list())
    print(save.load_train_types_dict())
