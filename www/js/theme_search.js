const backend = "/cgi-bin/theme_search.py"

$( document ).ready(function() {
    console.log("Running")
    populate_mugshots(undefined)
    $("#searchbox").keyup(update_search)

})

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

        div.append(`<div class="mugwrapper d-inline-block position-relative" id="${name_id}"><span class="collapse badge position-absolute top-100 start-50 text-light p-1 bg-danger">100</span><img class="mugshot" src="${image_data["url"]}" title="${image_data["name"]}" height="75px"></div>`)

    }

}

function update_search() { 
    search_text = $("#searchbox").val()

    if (search_text.length < 3) {
        $(".mugshot").removeClass("faded")
        $("span").hide()
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

    // Reset any previous results
    $(".mugshot").addClass("faded")
    $("span").hide()

    // First go through the keys to grey out any 
    // group leaders with no hits.

    for (let [name,hits] of Object.entries(data)) {

        name_id = name.toLowerCase()
        name_id = name_id.replaceAll(" ","_")

        $("#"+name_id).find("img").removeClass("faded")

        hit_count = hits.length
        $("#"+name_id).find("span").show()
        $("#"+name_id).find("span").text(hit_count)


    }


}


}