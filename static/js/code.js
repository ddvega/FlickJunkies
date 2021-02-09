let poster = "";
let tmdbID = "";
let overview = "";
let genre = "";
let lang = "";
let title = "";
let date = "";
let rating = "";
let cast = "";

$('[data-toggle="collapse"]').on('click', function () {
    var $this = $(this),
        $parent = typeof $this.data('parent') !== 'undefined' ? $($this.data('parent')) : undefined;
    if ($parent === undefined) { /* Just toggle my  */
        $this.find('.glyphicon').toggleClass('glyphicon-plus glyphicon-minus');
        return true;
    }

    /* Open element will be close if parent !== undefined */
    var currentIcon = $this.find('.glyphicon');
    currentIcon.toggleClass('glyphicon-plus glyphicon-minus');
    $parent.find('.glyphicon').not(currentIcon).removeClass('glyphicon-minus').addClass('glyphicon-plus');

});


// dynamically shows, in navbar, the title name of the book being viewed
function loadListName(l) {
    console.log(l);
    document.getElementById('listName').innerHTML = l;

}


function passArrFromTMDB(listID) {
    $.ajax({
        url: "/addFromTMDB/",
        headers: {"X-CSRFToken": window.CSRF_TOKEN},
        type: "POST",
        data: {
            'poster': poster,
            'tmdbID': tmdbID,
            'overview': overview,
            'genre': genre,
            'lang': lang,
            'title': title,
            'date': date,
            'rating': rating,
            'cast': cast,
            'listID': listID,
        },
    });
}

function load_details(p, g, l, t, d, r, o, m, c = "") {
    poster = p;
    overview = o;
    genre = g;
    lang = l;
    title = t;
    date = d;
    rating = r;
    tmdbID = m;
    cast = c;
    document.getElementById("search").style.display = 'none'

}


function get_local() {
    // show display when row is clicked
    document.getElementById('mydiv').style.display = 'block';

    // pass tmdbID from tmdbResults.html to detailWindow.html
    document.getElementById("comment").value = tmdbID

    // split string into an array
    cast_arr = cast.split(",");

    cast = cast_arr.join("\n");
    console.log(cast)

    // populate dom with poster and movie info
    show_detail_window();

}


function get_from_tmdb(key) {
    // show display when row is clicked
    document.getElementById('mydiv').style.display = 'block';
    // document.getElementById('collage').style.display = 'none';


    poster = "https://image.tmdb.org/t/p/w154" + poster;
    url = "https://api.themoviedb.org/3/movie/" + tmdbID + `/credits?api_key=${key}`;
    console.log(url)

    let castArray = [];

    console.log(castArray)

    $.getJSON(url, function (data) {
        if (cast === "") {
            for (x in data["cast"]) {
                castArray.push(data["cast"][x]["name"]);
            }
            cast = castArray.join("\n");
        }

        show_detail_window();
    });

}

function show_detail_window() {
    console.log(title)
    console.log("wtf")
    document.getElementById("poster").src = poster;
    document.getElementById("cast").innerText = cast;
    document.getElementById("description").innerText = overview;
    document.getElementById("rating").innerText = rating;
    document.getElementById("year").innerText = date;
    document.getElementById("lang").innerText = lang;
    document.getElementById("tab").className = "shortTable"
}

function show_search() {
    if (document.getElementById("search").style.display === 'block') {
        document.getElementById("search").style.display = 'none';
    } else {
        document.getElementById("search").style.display = 'block';

    }

}


