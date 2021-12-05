import requests
import json

def get_pokemons(index: int, file):
    main_url = "https://pokeapi.co/api/v2/pokemon/{index}".format(index=index)
    poke_req = requests.get(main_url)
    poke_data = json.loads(poke_req.text)
    species = poke_data["species"]["url"]
    spe_req = requests.get(species)
    spe_data = json.loads(spe_req.text)
    if spe_data["is_legendary"] is True:
        entry = "\"{name}\" : \"{rarity}\",".format(name=poke_data["name"], rarity="legendary")
    elif spe_data["is_mythical"] is True:
        entry = "\"{name}\" : \"{rarity}\",".format(name=poke_data["name"], rarity="mythical")
    else:
        entry = "\"{name}\" : \"{rarity}\",".format(name=poke_data["name"], rarity="common")

    file.write(entry)

def main():

    file = open("data/poke_rarity.json", "a")

    for i in range(381, 899):
        get_pokemons(i, file)
        if i%10 == 0:
            file.close()
            file = open("data/poke_rarity.json", "a")

    file.close()

if __name__ == "__main__":
    main()
