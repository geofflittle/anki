import yaml

if __name__ == "__main__":
    with open("van_sickles_modern_airmanship.yml") as f:
        notes = yaml.load(f, Loader=yaml.FullLoader)
        print(notes)
