// const wordEle = document.getElementById("word");
// const sectionEle = document.getElementById("section");
// const box = document.getElementById("box");

async function request(word, section, getString) {
    var base = "https://api.wordnik.com/v4/";
    var endpoint = "word.json";
    var url = `${base}${endpoint}/${word}/${section}?${getString}`;
    var response = await fetch(url);
    var responseText = await response.text();
    var responseJSON = JSON.parse(responseText);
    console.log(responseJSON)
}

function main() {
    var getList = [];
    for (var pair of location.search.substring(1).split("&")) {
        var split = pair.split("=");
        if (split[0] === "word") {
            // wordEle.innerText = split[1];
            var word = split[1];
        } else if (split[0] == "section") {
            // sectionEle.innerText = split[1];
            var section = split[1];
        } else {
            getList.push(pair);
        }
    }
    var getString = getList.join("&");
    request()
}

document.addEventListener("DOMContentLoaded", main);
