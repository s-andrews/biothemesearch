const backend = "cgi-bin/theme_search.py"
var name_translation = {}

// Gives the hand crafted description of their work
var person_descriptions = {}

// Stores the current search results
let search_results = ""

// Stores the set of key search terms and which group leaders they apply to
let key_terms = ""

$( document ).ready(function() {
    console.log("Running")
    populate_mugshots(undefined)

    populate_key_terms(undefined)

    populate_person_descriptions()

    $("#searchbox").keyup(function(){$(".keyterm").removeClass("highlightterm");update_search()})
    $("#clear").click(function(){$("#person_description").text("");$("#personname").text("Babraham Research Interest Search");$("#searchbox").val("");$(".keyterm").removeClass("highlightterm");update_search()})
})

function show_snippets() {
    // If they've clicked on a faded icon then don't do anything
    if ($(this).hasClass("faded")) {
        return
    }

    let short_name = $(this).parent().attr("id")
    let long_name = name_translation[short_name]

    $("#personname").html(long_name)
    console.log("Clicked on "+short_name)

    if (! search_results) {
        // There isn't a search result so instead we'll 
        // highlight the key terms for the group leader
        // they just clicked on

        // We can add their hand crafted description
        $("#person_description").html(person_descriptions[short_name])

        let ktspans = $(".keyterm")

        // Remove any existing highlights
        ktspans.removeClass("highlightterm")

        for (let i=0;i<ktspans.length;i++) {
            let thisterm = ktspans.eq(i).text()
            // Check whether this gl is associated with that term
            if (key_terms[thisterm].includes(short_name)) {
                ktspans.eq(i).addClass("highlightterm")
            }
        }

        return
    }

    // There are search results so clear any description which is showing
    $("#person_description").html("")

    // See if we have any snippet data for them stored
    for (let [name,hits] of Object.entries(search_results)) {
        name_id = name.toLowerCase()
        name_id = name_id.replaceAll(" ","_")
        name_id = name_id.replaceAll("'","")

        if (name_id != short_name) {
            continue
        }

        let snippets = $("#snippets")
        //  Clear the existing snippets
        snippets.text("")

        // Add their name
        $("#personname").html(name)

        for (let i in hits) {
            hit = hits[i]
            snippet_html = ""

            for (let j in hit["snippets"]) {
                snippet_html += `<div class="snippet">...${hit["snippets"][j]}...</div>`
            }


            snippets.append(`
            <div class="container mb-3">
            <h5><a target="_pubmed" href="https://pubmed.ncbi.nlm.nih.gov/${hit["pmid"]}">${hit["title"]}</a></h5>
            ${snippet_html}
            </div>`)
        }
    }


}

function populate_mugshots(data) {
    console.log("Populating mugshots")
    // Adds the various mugshots to the #mugshots div

    // The function can either be called with an undefined
    // value which will kick off an ajax request to get the
    // list of group leader mugshots, or it can be called 
    // by the ajax callback, in which case data will be the 
    // json list of group leaders

    if (typeof(data) === 'undefined') {
        // We need to query for the submission data
        $.ajax(
            {
                url: backend,
                data: {
                    action: "mugshots"
                },
                success: function(data) {
                    populate_mugshots(data)
                },
                error: function(message) {
                    console.log("Failed to list group leaders "+message)
                }
            }
        )
        return
    }

    // We have actual data so fill in the mugshots

    div = $("#mugshots")

    for (i in data) {
        image_data = data[i]
        console.log("Adding "+image_data["name"])

        // We need a lowercase version of name with no spaces to act
        // as an id tag
        name_id = image_data["name"].toLowerCase()
        name_id = name_id.replaceAll(" ","_")
        name_id = name_id.replaceAll("'","")

        name_translation[name_id] = image_data["name"]

        div.append(`<div class="mugwrapper d-inline-block position-relative" id="${name_id}"><span class="collapse badge position-absolute top-100 start-50 text-light p-1 bg-danger">100</span><img class="mugshot" src="${image_data["url"]}" title="${image_data["name"]}" height="75px"></div>`)

    }

    // Add callbacks to these new objects
    $(".mugshot").click(show_snippets)
 
}

function populate_key_terms(data) {
    console.log("Populating key terms")
    // Adds the key terms to the opening screen

    // The function can either be called with an undefined
    // value which will kick off an ajax request to get the
    // list of group leader mugshots, or it can be called 
    // by the ajax callback, in which case data will be the 
    // json list of group leaders

    if (typeof(data) === 'undefined') {
        // We need to query for the submission data
        $.ajax(
            {
                url: backend,
                data: {
                    action: "keyterms"
                },
                success: function(data) {
                    populate_key_terms(data)
                },
                error: function(message) {
                    console.log("Failed to list group leaders "+message)
                }
            }
        )
        return
    }

    // We have actual data so fill in the key terms
    key_terms = data

    div = $("#keyterms")

    let terms = Object.keys(data)
    terms.sort()
    for (i in terms) {
        div.append(` <span class="keyterm">${terms[i]}</span>`)
    }

    // Add callbacks to these new objects
    $(".keyterm").click(select_key_term)
 
}

function populate_person_descriptions() {
    console.log("Populating person descriptions terms")
    // Stores the hand crafted person descriptions so 
    // we can show them later
    // We need to query for the submission data
    $.ajax(
        {
            url: backend,
            data: {
                action: "descriptions"
            },
            success: function(data) {
                person_descriptions = data
            },
            error: function(message) {
                console.log("Failed to get descriptions "+message)
            }
        }
    )
}



function select_key_term() {
    let term = $(this).text()

    $("#searchbox").val(term)
    update_search()
}


function update_search() { 
    search_text = $("#searchbox").val()

    $("#snippets").text("")
    $("#personname").text("Babraham Research Interest Search")
    $("#person_description").html("")

    if (search_text.length < 3) {
        $(".mugshot").removeClass("faded")
        $(".badge").hide()
        $("#keyterms").show()
        search_results = ""
        return
    }
    console.log("Searching with "+search_text)

    $.ajax(
        {
            url: backend,
            data: {
                action: "search",
                term: search_text
            },
            success: function(data) {
                add_search_results(data)
            },
            error: function(message) {
                console.log("Failed to run search "+message)
            }
        }
    )

function add_search_results(data) {
    // Data is a dict with names as keys and a list
    // as value with a dict with title and snippets
    // in it.

    // Store these results so we can show snippets
    search_results = data

    // Reset any previous results
    $(".mugshot").addClass("faded")
    $(".badge").hide()
    $("#keyterms").hide()

    // Go through and highlight group leaders with hits

    for (let [name,hits] of Object.entries(data)) {

        name_id = name.toLowerCase()
        name_id = name_id.replaceAll(" ","_")
        name_id = name_id.replaceAll("'","")

        $("#"+name_id).find("img").removeClass("faded")

        hit_count = hits.length
        $("#"+name_id).find("span").show()
        $("#"+name_id).find("span").text(hit_count)

    }


}


}
