function chosenDocs() {
	data = {}
	let check = true
	$(".docs-data").each(function() {
		id = this.id

		if (!$(this).find(".delivered").prop("checked") && $(this).find(".sent").prop("checked")) {
			alert("Nie można wysłać niedostarczonego dokumentu.")
			check = false
		} else if (!$(this).find(".sent").prop("checked") && $(this).find(".sent-date").val()!=="") {
			alert("Zaznaczona data wysyłki dokumentu, który nie został wysłany.")
			check =  false
		} else if ($(this).find(".sent").prop("checked") && $(this).find(".sent-date").val()==="") {
			withoutDate = window.confirm("Dokument wysłany do kadr bez zaznaczonej daty.\nKontynuować?")
			if (!withoutDate) {
				check =  false
			}
		};

		data[id] = {
			"delivered": $(this).find(".delivered").prop("checked"),
			"sent": $(this).find(".sent").prop("checked"),
			"sent-date": $(this).find(".sent-date").val(),
			"notes": $(this).find(".notes").val()
		}
	});
	if (check === true) {
		return data
	} else {
		return false
	}
}

$(document).ready(function() {
    $("#change-start-docs-status").submit(function(e){
        let form = $(this);
        $.ajax({
            url   : form.attr("action"),
            type  : form.attr("method"),
            contentType: "application/json;charset=UTF-8",
            data  : JSON.stringify(chosenDocs()),
            success: function(response){
					if (response.response) {
            			window.location.replace(response.response);
            		} else {
            			alert("Sprawdź formularz jeszcze raz.\nZnaleziono nieprawidłowości.")
            		}
            },
        });
        return false;
    });
});
