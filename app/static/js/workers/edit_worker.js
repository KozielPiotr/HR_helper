function basicInfo() {
	data = {
		"worker_id": $("#worker-id").val(),
		"name": $("#name").val(),
		"workplace_id": $("#workplace").val(),
		"function_id": $("#function").val(),
		"contract_begin": $("#contract-begin").val(),
		"contract_end": $("#contract-end").val(),
		"works": $("#still-works").val(),
		"work_end": $("#work-end").val()
	}
	if (data.works==="False" && data.work_end === "") {
		correct = confirm("Zaznaczono, że pracownik już nie pracuje, a nie określono daty rozwiązania umowy.\nTak powinno byc?")
		if (!correct) {
		data["OK"] = false
			return data
		}
	} else if (data.works === "True" && data.work_end !== "") {
		correct = confirm("Zaznaczono, że pracownik nadal pracuje, a wprowadzono datę rozwiązania umowy.\nTak powinno być?")
		if (!correct) {
			data["OK"] = false
			return data
		}
	}
	data["OK"] = true
	return data
}

$(document).ready(function() {
    $("#change-basic").submit(function(e){
        let form = $(this);
        $.ajax({
            url   : form.attr("action"),
            type  : form.attr("method"),
            contentType: "application/json;charset=UTF-8",
            data  : JSON.stringify(basicInfo()),
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
