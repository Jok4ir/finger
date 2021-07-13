(() => {
  $("#subm").on("click", (e) => {
    // console.log("clicked");
    e.preventDefault();
    let name = $("#name")[0].value;
    let firstname = $("#firstname")[0].value;
    let cin = $("#cin")[0].value;
    let sex = $("#sex")[0].value;
    let age = $("#age")[0].value;
    let situation = $("#situation")[0].value;
    let photo = document.getElementById("file").files[0];

    var file_data = $("#file").prop("files")[0];
    const files = document.querySelector("[type=file]").files;
    const fileToUpload = files[0];

    const info = {
      name: name,
      firstName: firstname,
      cin: cin,
      sex: sex,
      age: age,
      situation: situation,
      // file: photo
    };

    $.post(
      "http://localhost:5000/enroll",
      {
        name: name,
        firstName: firstname,
        cin: cin,
        sex: sex,
        age: age,
        situation: situation,
        // file: photo
      },
      (result) => {
        console.log(result);
        console.log("uploading the file");
        var form_data = new FormData();
        // form_data.append('file', file_data);
        form_data.append("files[]", fileToUpload);
        // alert(form_data);
        $.ajax({
          url: "http://localhost:5000/upload",
          dataType: "text",
          cache: false,
          contentType: false,
          processData: false,
          data: form_data,
          type: "post",
          success: function (script_response) {},
        });
        // fetch('http://localhost:5000/upload', {
        //     method: 'POST',
        //     body: form_data
        // }).then((resp) => {
        //     console.log("response")
        // })
      }
    );
  });

  $("#uploadfile").on("click", (e) => {
    const files = document.querySelector("[type=file]").files;
    var form_data2 = new FormData();
    const fileToUpload = files[0];
    console.log(files)
    form_data2.append("file", fileToUpload);
    console.log(form_data2)
    fetch("http://localhost:5000/upload", {
      method: "POST",
      body: form_data2,
    }).then((resp) => {
      console.log(resp);
    });
  });
})();
