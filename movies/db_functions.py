import requests
from credentials import *
import datetime


def package_tmdb_data(jsonResponse, dictKey):
    movie_list = []

    try:
        for i in range(len(jsonResponse[dictKey])):
            s = jsonResponse[dictKey][i]

            movie_list.append(
                {
                    "poster": s["poster_path"],
                    "id": s["id"],
                    "genre": getGenre(s["genre_ids"][0]),
                    "lang": get_language(s["original_language"]),
                    "title": s["title"].replace("'", "`"),
                    "date": s["release_date"][:4],
                    "rating": s["vote_average"],
                    "overview": s["overview"].replace("'", "`"),
                }
            )
    except:
        print("search error")

    return sorted(movie_list, key=lambda x: x["rating"], reverse=True)


def id_actor_get(actorName):
    """Fetches the ID of an actor by querying the TMDB database."""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/search/person?api_key="
            + api_key
            + f"&language=en-US&query={actorName}&page=1&include_adult=false"
        )
        searchResponse = response.json()
        actorID = searchResponse["results"][0]["id"]
        return actorID

    except:
        print("no results")


def update_ratings(tmdb_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key="
            + api_key
            + "&language=en-US"
        )
        details = response.json()

        return details["vote_average"]
    except:
        print("couldn't get rating")
        return None


def tmdb_discover(actor=None, title=None, genre=None, year=None, page=1):
    if title:
        return tmdb_title_search(title)

    reqString = (
        "https://api.themoviedb.org/3/discover/movie?api_key="
        + api_key
        + f"&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page={page}"
    )

    if year:
        print(year)
        reqString = reqString + f"&primary_release_year={year}"

    if actor:
        keyID = id_actor_get(actor)
        print(keyID)
        reqString = reqString + f"&with_people={keyID}"

    if genre:
        genID = id_genre_get(genre)
        print(genID)
        reqString = reqString + f"&with_genres={genID}"

    response = requests.get(reqString)
    data = response.json()

    return package_tmdb_data(data, "results")


def tmdb_actor_search(actorName):
    """Finds an actor in the TMDB database."""
    keyID = id_actor_get(actorName)
    print(keyID)
    response = requests.get(
        f"https://api.themoviedb.org/3/person/{keyID}/movie_credits?api_key="
        + api_key
        + "&language=en-US"
    )
    actors = response.json()

    return package_tmdb_data(actors, "cast")


def tmdb_title_search(keyword):
    """Finds an actor in the TMDB database."""
    response = requests.get(
        "https://api.themoviedb.org/3/search/movie?api_key="
        + api_key
        + f"&language=en-US&query={keyword}&page=1&include_adult=false"
    )
    mov = response.json()
    return package_tmdb_data(mov, "results")


def getGenre(genreID):
    """Converts id obtained from TMDB to a genre name"""
    genreDict = [
        {"id": 28, "name": "Action"},
        {"id": 12, "name": "Adventure"},
        {"id": 16, "name": "Animation"},
        {"id": 35, "name": "Comedy"},
        {"id": 80, "name": "Crime"},
        {"id": 99, "name": "Documentary"},
        {"id": 18, "name": "Drama"},
        {"id": 10751, "name": "Family"},
        {"id": 14, "name": "Fantasy"},
        {"id": 36, "name": "History"},
        {"id": 27, "name": "Horror"},
        {"id": 10402, "name": "Music"},
        {"id": 9648, "name": "Mystery"},
        {"id": 10749, "name": "Romance"},
        {"id": 878, "name": "Science Fiction"},
        {"id": 10770, "name": "TV Movie"},
        {"id": 53, "name": "Thriller"},
        {"id": 10752, "name": "War"},
        {"id": 37, "name": "Western"},
    ]

    for i in genreDict:
        if i.get("id") == genreID:
            return i.get("name")


def id_genre_get(genre):
    genreDict = [
        {"id": 28, "name": "Action"},
        {"id": 12, "name": "Adventure"},
        {"id": 16, "name": "Animation"},
        {"id": 35, "name": "Comedy"},
        {"id": 80, "name": "Crime"},
        {"id": 99, "name": "Documentary"},
        {"id": 18, "name": "Drama"},
        {"id": 10751, "name": "Family"},
        {"id": 14, "name": "Fantasy"},
        {"id": 36, "name": "History"},
        {"id": 27, "name": "Horror"},
        {"id": 10402, "name": "Music"},
        {"id": 9648, "name": "Mystery"},
        {"id": 10749, "name": "Romance"},
        {"id": 878, "name": "Science Fiction"},
        {"id": 10770, "name": "TV Movie"},
        {"id": 53, "name": "Thriller"},
        {"id": 10752, "name": "War"},
        {"id": 37, "name": "Western"},
    ]
    for i in genreDict:
        if i.get("name").lower() == genre:
            return i.get("id")


def clean_movie_objects(movs):
    data = []
    actor_list = []

    for m in range(len(movs)):
        temp = ""
        actor = movs[m].actors.all()
        for a in range(len(actor)):
            act = actor[a].name.replace("'", "\\'")
            if a == len(actor) - 1:
                temp += act
            else:
                temp += act + ','
        actor_list.append(temp)

    for m in range(len(movs)):
        temp = {}
        temp["id"] = movs[m].id
        temp["genre"] = movs[m].genre.genreName
        temp["lang"] = movs[m].lang.languageName
        temp["title"] = movs[m].title
        temp["date"] = movs[m].years.yearDate
        temp["rating"] = movs[m].rating
        temp["poster"] = movs[m].poster
        temp["overview"] = movs[m].overview
        temp["tmdbID"] = movs[m].tmdbID
        temp["cast"] = actor_list[m]

        data.append(temp)

    return data


def cleanListObjects(dirtyList, users):
    data = []

    for dirt in dirtyList:
        temp = {}
        u = users.objects.get(id=dirt.user_id)
        temp["id"] = dirt.id
        temp["listName"] = dirt.listName
        temp["user"] = u
        temp["private"] = dirt.private
        temp["count"] = dirt.movies.count()
        data.append(temp)

    return data


def cleanCommentObject(comment, users):
    data = []

    for l in comment:
        temp = {}
        u = users.objects.get(id=l.user_id)
        temp["id"] = l.id
        temp["body"] = l.body
        temp["user"] = u

        temp["date"] = l.date
        temp["spoiler"] = l.spoiler
        data.append(temp)

    return data


def get_language(code):
    lang_dict = [
        {"id": "ab", "name": "Abkhazian"},
        {"id": "aa", "name": "Afar"},
        {"id": "af", "name": "Afrikaans"},
        {"id": "ak", "name": "Akan"},
        {"id": "sq", "name": "Albanian"},
        {"id": "am", "name": "Amharic"},
        {"id": "ar", "name": "Arab"},
        {"id": "an", "name": "Aragonese"},
        {"id": "hy", "name": "Armenian"},
        {"id": "as", "name": "Assamese"},
        {"id": "av", "name": "Avaric"},
        {"id": "ae", "name": "Avestan"},
        {"id": "ay", "name": "Aymara"},
        {"id": "az", "name": "Azerbaijani"},
        {"id": "bm", "name": "Bambara"},
        {"id": "ba", "name": "Bashkir"},
        {"id": "eu", "name": "Basque"},
        {"id": "be", "name": "Belarusian"},
        {"id": "bn", "name": "Bengali"},
        {"id": "bh", "name": "Bihari"},
        {"id": "bi", "name": "Bislama"},
        {"id": "bs", "name": "Bosnian"},
        {"id": "br", "name": "Breton"},
        {"id": "bg", "name": "Bulgarian"},
        {"id": "my", "name": "Burmese"},
        {"id": "ca", "name": "Catalan"},
        {"id": "ch", "name": "Chamorro"},
        {"id": "ce", "name": "Chechen"},
        {"id": "ny", "name": "Chichewa"},
        {"id": "zh", "name": "Chinese"},
        {"id": "cv", "name": "Chuvash"},
        {"id": "kw", "name": "Cornish"},
        {"id": "co", "name": "Corsican"},
        {"id": "cr", "name": "Cree"},
        {"id": "hr", "name": "Croatian"},
        {"id": "cs", "name": "Czech"},
        {"id": "da", "name": "Danish"},
        {"id": "dv", "name": "Divehi"},
        {"id": "nl", "name": "Dutch"},
        {"id": "dz", "name": "Dzongkha"},
        {"id": "en", "name": "English"},
        {"id": "eo", "name": "Esperanto"},
        {"id": "et", "name": "Estonian"},
        {"id": "ee", "name": "Ewe"},
        {"id": "fo", "name": "Faroese"},
        {"id": "fj", "name": "Fijian"},
        {"id": "fi", "name": "Finnish"},
        {"id": "fr", "name": "French"},
        {"id": "ff", "name": "Fulah"},
        {"id": "gl", "name": "Galician"},
        {"id": "ka", "name": "Georgian"},
        {"id": "de", "name": "German"},
        {"id": "el", "name": "Greek"},
        {"id": "gn", "name": "Guarani"},
        {"id": "gu", "name": "Gujarati"},
        {"id": "ht", "name": "Haitian"},
        {"id": "ha", "name": "Hausa"},
        {"id": "he", "name": "Hebrew"},
        {"id": "hz", "name": "Herero"},
        {"id": "hi", "name": "Hindi"},
        {"id": "ho", "name": "Hiri Motu"},
        {"id": "hu", "name": "Hungarian"},
        {"id": "ia", "name": "Interlingua"},
        {"id": "id", "name": "Indonesian"},
        {"id": "ie", "name": "Interlingue"},
        {"id": "ga", "name": "Irish"},
        {"id": "ig", "name": "Igbo"},
        {"id": "ik", "name": "Inupiaq"},
        {"id": "io", "name": "Ido"},
        {"id": "is", "name": "Icelandic"},
        {"id": "it", "name": "Italian"},
        {"id": "iu", "name": "Inuktitut"},
        {"id": "ja", "name": "Japanese"},
        {"id": "jv", "name": "Javanese"},
        {"id": "kl", "name": "Kalaallisut"},
        {"id": "kn", "name": "Kannada"},
        {"id": "kr", "name": "Kanuri"},
        {"id": "ks", "name": "Kashmuri"},
        {"id": "kk", "name": "Kazakh"},
        {"id": "km", "name": "Central Khmer"},
        {"id": "ki", "name": "Kikuyu"},
        {"id": "rw", "name": "Kinyarwanda"},
        {"id": "ky", "name": "Kirghiz"},
        {"id": "kv", "name": "Komi"},
        {"id": "kg", "name": "Kongo"},
        {"id": "ko", "name": "Korean"},
        {"id": "ku", "name": "Kurdish"},
        {"id": "kj", "name": "Kuanyama"},
        {"id": "la", "name": "Latin"},
        {"id": "lb", "name": "Luxembourgish"},
        {"id": "lg", "name": "Ganda"},
        {"id": "li", "name": "Limburgan"},
        {"id": "ln", "name": "Lingala"},
        {"id": "lo", "name": "Lao"},
        {"id": "lt", "name": "Lithuanian"},
        {"id": "lu", "name": "Luba-Katanga"},
        {"id": "lv", "name": "Latvian"},
        {"id": "gv", "name": "Manx"},
        {"id": "mk", "name": "Macedonian"},
        {"id": "mg", "name": "Malagasy"},
        {"id": "ms", "name": "Malay"},
        {"id": "ml", "name": "Malayalam"},
        {"id": "mt", "name": "Maltese"},
        {"id": "mi", "name": "Maori"},
        {"id": "mr", "name": "Marathi"},
        {"id": "mh", "name": "Marshallese"},
        {"id": "mn", "name": "Mongolian"},
        {"id": "na", "name": "Nauru"},
        {"id": "nv", "name": "Navajo"},
        {"id": "nd", "name": "North Ndebele"},
        {"id": "ne", "name": "Nepali"},
        {"id": "ng", "name": "Ndonga"},
        {"id": "nb", "name": "Norwegian Bokmal"},
        {"id": "nn", "name": "Norwegian Nynorsk"},
        {"id": "no", "name": "Norwegian"},
        {"id": "ii", "name": "Sichuan Yi"},
        {"id": "nr", "name": "South Ndebele"},
        {"id": "oc", "name": "Occitan"},
        {"id": "oj", "name": "Ojibwa"},
        {"id": "cu", "name": "Church Slavic"},
        {"id": "om", "name": "Oromo"},
        {"id": "or", "name": "Oriya"},
        {"id": "os", "name": "Ossetian"},
        {"id": "pa", "name": "Punjabi"},
        {"id": "pi", "name": "Pali"},
        {"id": "fa", "name": "Persian"},
        {"id": "pl", "name": "Polish"},
        {"id": "ps", "name": "Pashto"},
        {"id": "pt", "name": "Portuguese"},
        {"id": "qu", "name": "Quechua"},
        {"id": "rm", "name": "Romansh"},
        {"id": "rn", "name": "Rundi"},
        {"id": "ro", "name": "Romanian"},
        {"id": "ru", "name": "Russian"},
        {"id": "sa", "name": "Sanskrit"},
        {"id": "sc", "name": "Sardinian"},
        {"id": "sd", "name": "Sindhi"},
        {"id": "se", "name": "Northern Sami"},
        {"id": "sm", "name": "Samoan"},
        {"id": "sg", "name": "Sango"},
        {"id": "sr", "name": "Serbian"},
        {"id": "gd", "name": "Gaelic"},
        {"id": "sn", "name": "Shona"},
        {"id": "si", "name": "Sinhala"},
        {"id": "sk", "name": "Slovak"},
        {"id": "sl", "name": "Slovenian"},
        {"id": "so", "name": "Somali"},
        {"id": "st", "name": "Southern Sotho"},
        {"id": "es", "name": "Spanish"},
        {"id": "su", "name": "Sudanese"},
        {"id": "sw", "name": "Swahili"},
        {"id": "ss", "name": "Swati"},
        {"id": "sv", "name": "Swedish"},
        {"id": "ta", "name": "Tamil"},
        {"id": "te", "name": "Telugu"},
        {"id": "tg", "name": "Tajik"},
        {"id": "th", "name": "Thai"},
        {"id": "ti", "name": "Tigrinya"},
        {"id": "bo", "name": "Tibetan"},
        {"id": "tk", "name": "Turkmen"},
        {"id": "tl", "name": "Tagalog"},
        {"id": "tn", "name": "Tswana"},
        {"id": "to", "name": "Tonga"},
        {"id": "tr", "name": "Turkish"},
        {"id": "ts", "name": "Tsonga"},
        {"id": "tt", "name": "Tatar"},
        {"id": "tw", "name": "Twi"},
        {"id": "ty", "name": "Tahitian"},
        {"id": "ug", "name": "Uighur"},
        {"id": "uk", "name": "Ukranian"},
        {"id": "ur", "name": "Urdu"},
        {"id": "uz", "name": "Uzbek"},
        {"id": "ve", "name": "Venda"},
        {"id": "vi", "name": "Vietnamese"},
        {"id": "vo", "name": "Volapuk"},
        {"id": "wa", "name": "Walloon"},
        {"id": "cy", "name": "Welsh"},
        {"id": "wo", "name": "Wolof"},
        {"id": "fy", "name": "Western Frisian"},
        {"id": "xh", "name": "Xhosa"},
        {"id": "yi", "name": "Yiddish"},
        {"id": "yo", "name": "Yoruba"},
        {"id": "za", "name": "Zhuang"},
        {"id": "zu", "name": "Zulu"},
    ]

    for i in lang_dict:
        if i.get("id").lower() == code:
            return i.get("name")
