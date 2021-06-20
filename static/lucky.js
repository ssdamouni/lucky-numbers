/** processForm: get data from form and make AJAX call to our API. */

async function processForm(evt) {
    evt.preventDefault();

    let name = $("#name").val();
    let email = $("#email").val();
    let year = $("#year").val();
    let color = $("#color").val();
    
    res = await axios.post('http://127.0.0.1:5000/api/get-lucky-num', {
        "name": name,
	    "email": email,
	    "year": year,
	    "color": color
    });
    console.log(res);
    handleResponse(res);
}

/** handleResponse: deal with response from our lucky-num API. */

function handleResponse(resp) {
    if (resp.status == 202){
        const fields = ["name", "email", "year", "color"] 
        let errors = resp.data
        for (let error in errors){
            for (let field in fields){
                if (error == fields[field]){
                    console.log(errors[error][0]);
                    $(`#${error}-err`).text(errors[error][0]);
                }
            }
        }
    }
    if (resp.status == 201){        
        $("#lucky-results").text(
            `Your lucky number is ${resp.data.num.num}. ${resp.data.num.fact}.  
            Your birth year is ${resp.data.year.num}. ${resp.data.year.fact}.`);
        $( '#lucky-form' ).each(function(){
                this.reset();
        });
        $("#name-err").text("");
        $("#year-err").text("");
        $("#email-err").text("");
        $("#color-err").text("");
    }
};


$("#lucky-form").on("submit", processForm);
