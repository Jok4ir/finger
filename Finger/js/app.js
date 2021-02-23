(() => {
    $("#subm").on("click", (e) => {
        console.log("clicked")
        e.preventDefault();
        let name = $("#name")[0].value
        let firstname = $("#firstname")[0].value
        let cin = $("#cin")[0].value
        let sex = $("#sex")[0].value
        let age = $("#age")[0].value
        let situation = $("#situation")[0].value
        let photo = document.getElementById('file').files[0]

        var file_data = $('#file').prop('files')[0];  

        const info = {
            name: name,
            firstName: firstname,
            cin: cin,
            sex: sex,
            age: age,
            situation: situation,
            // file: photo
        }

        $.post("http://localhost:5000/enroll", {
            name: name,
            firstName: firstname,
            cin: cin,
            sex: sex,
            age: age,
            situation: situation,
            // file: photo
        }, (result) => {
            console.log(result)
            console.log("uploading the file")
            var form_data = new FormData();                  
            form_data.append('file', file_data);
            // alert(form_data);                             
            $.ajax({
                url: 'http://localhost:5000/upload', 
                dataType: 'text',  
                cache: false,
                contentType: false,
                processData: false,
                data: form_data,                         
                type: 'post',
                success: function(script_response){
                    
                }
            });
        })
    })
})()
