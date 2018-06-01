const wordEle = document.getElementById("wordEle");
const sectionEle = document.getElementById("sectionEle");
const box = document.getElementById("box");

function displayInfo(section, response) {
    switch (section) {
    case "audio":
        for (var audio of response) {
            var quote = document.createElement("blockquote");
            var media = document.createElement("video");
            media.setAttribute("controls", "");
            media.src = audio.fileUrl;
            quote.append(media);
            var attribute = document.createElement("span");
            attribute.innerText = audio.attributionText;
            quote.append(attribute);
            box.append(quote);
        }
    case "frequency":
        var ctx = document.createElement("canvas");
        box.append(ctx)
        var count = [];
        var labels = [];
        for (frequent of response["frequency"]) {
            count.push(frequent["count"]);
            labels.push(frequent["year"]);
        }
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Frequency",
                    data: count
                }]
            }
        });
    }
}

async function request(word, section, getString) {
    var base = "https://api.wordnik.com/v4/";
    var endpoint = "word.json";
    var url = `${base}${endpoint}/${word}/${section}?${getString}`;
    var response = await fetch(url);
    var responseText = await response.text();
    var responseJSON = JSON.parse(responseText);
    displayInfo(section, responseJSON);
}

function main() {
    var getList = [];
    var temp = {};
    for (var pair of location.search.substring(1).split("&")) {
        var split = pair.split("=");
        if (split[0] === "word") {
            wordEle.innerText = split[1];
            temp["word"] = split[1];
        } else if (split[0] === "section") {
            sectionEle.innerText = split[1];
            temp["section"] = split[1];
        } else {
            getList.push(pair);
        }
    }
    var getString = getList.join("&");
    request(temp["word"], temp["section"], getString);
}

document.addEventListener("DOMContentLoaded", main);
