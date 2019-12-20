function get_tableau_token(tokenURI) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: tokenURI,
            complete: function(jqXHR, textStatus) {
                resolve(jqXHR.responseJSON);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                reject(textStatus);
            },
        });

    });
}

$.fn.the = function() {
    if (this.length === 1) {
        return $(this)[0];
    } else {
        throw new Error("Expected 1 value in jQuery object, got " + this.length)
    }
}