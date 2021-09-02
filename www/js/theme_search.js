const backend = "/cgi-bin/theme_search.py"

$( document ).ready(function() {
    console.log("Running")
    populate_mugshots(undefined)
    $("#searchbox").keypress(update_search)

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

        div.append(`<img src="${image_data["url"]}" title="${image_data["name"]}" height="100px">`)

    }

}

function update_search() {

}