
function chosenDocs() {
	choices = []
	$(".doc").each(function() {
		let choice = $(this).find("input[type='checkbox']")
		if (choice.prop('checked')){
			choices.push(choice.val())
		};
	});
	return choices
}

$(document).ready(function() {
    $("form").submit(function(e){
        let form = $(this);
        $.ajax({
            url   : form.attr("action"),
            type  : form.attr("method"),
            contentType: 'application/json;charset=UTF-8',
            data  : JSON.stringify(chosenDocs()),
            success: function(response){
                window.location.replace(response);
            },
        });
        return false;
    });
});
