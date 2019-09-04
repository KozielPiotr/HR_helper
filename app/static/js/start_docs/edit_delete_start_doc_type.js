$(document).ready(function() {
    $(".submit-doc-changes").click(function(){
    	data = {
    	"name": $(this).closest("tr").find(".doc-name").val(),
    	"changed": $(this).closest("tr").find(".changed").val()
    	};

    	if (data.name != data.changed) {
    		$.ajax({
            url   : "/edit-start-doc-type",
            type  : "post",
            contentType: "application/json;charset=UTF-8",
            data  : JSON.stringify(data),
            success: function(response){
					if (response === "OK") {
						alert(`"${data.name}" zamieniono na "${data.changed}"`);
						location.reload();
					} else {
						alert("Coś poszło nie tak\nMoże taki dokument już istnieje?")
						location.reload();
					};
            },
        });
    	}
    })
})


$(document).ready(function() {
    $(".del-doc-type").click(function(){
		let type_id = $(this).closest("td").find(".doc-id").val();
		let url = $(this).closest("td").find(".del-url").val();
		window.location.replace(url)
    });
})