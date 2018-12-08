function processCreateAppointment() {
   var form = this.document.getElementById("f1");
   var array = jQuery(form).serializeArray();
   var jsondata = {};

   jQuery.each(array, function() {
     jsondata[this.name] = this.value || '';
   });

   $.ajax({
      url: 'http://localhost:5000/appointment',
      data: JSON.stringify(jsondata),
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      success: function(response) {
        resp = JSON.stringify(response);
        if(response.status == '204')
          alert(response.MESSAGE+" Appointment Not Created");
        else
          alert(resp+" APPOINTMENT CREATED")
        console.log(resp);
      },
      error: function(error) {
        console.log(error);
      }
    });
}

function processGetPhysicians() {
   $.ajax({
      url: 'http://localhost:5000/doctors',
      type: 'GET',
      dataType: 'json',
      contentType: 'application/json',
      success: function(response) {
        resp = JSON.stringify(response);
        alert(resp);
        console.log(resp);
      },
      error: function(error) {
        console.log(error);
      }
    });
}
