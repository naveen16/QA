function processCreateSession() {
   var form = this.document.getElementById("f1");
   var array = jQuery(form).serializeArray();
   var jsondata = {};

   jQuery.each(array, function() {
     jsondata[this.name] = this.value || '';
   });

   $.ajax({
      url: 'http://localhost:5000/qa',
      data: JSON.stringify(jsondata),
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      success: function(response) {
        resp = JSON.stringify(response);
        alert(resp+" SESSION CREATED");
        console.log(resp);
      },
      error: function(error) {
        console.log(error);
      }
    });
}

function processCreateQuestion() {
   var form = this.document.getElementById("f2");
   var array = jQuery(form).serializeArray();
   var jsondata = {};

   jQuery.each(array, function() {
     jsondata[this.name] = this.value || '';
   });

   $.ajax({
      url: 'http://localhost:5000/question/'+jsondata['sessionId'],
      data: JSON.stringify(jsondata),
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      success: function(response) {
        resp = JSON.stringify(response);
        alert(resp+" QUESTION CREATED");
        console.log(resp);
      },
      error: function(error) {
        console.log(error);
      }
    });
}

function processCreateAnswer() {
   var form = this.document.getElementById("f3");
   var array = jQuery(form).serializeArray();
   var jsondata = {};

   jQuery.each(array, function() {
     jsondata[this.name] = this.value || '';
   });

   $.ajax({
      url: 'http://localhost:5000/answer/'+jsondata['sessionId']+'/'+jsondata['questionId'],
      data: JSON.stringify(jsondata),
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      success: function(response) {
        resp = JSON.stringify(response);
        alert(resp+" ANSWER CREATED");
        console.log(resp);
      },
      error: function(error) {
        console.log(error);
      }
    });
}

function processGetSession() {
   var form = this.document.getElementById("f4");
   var array = jQuery(form).serializeArray();
   var jsondata = {};

   jQuery.each(array, function() {
     jsondata[this.name] = this.value || '';
   });

   $.ajax({
      url: 'http://localhost:5000/qa/'+jsondata['sessionId'],
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

function processGetQuestions() {
   var form = this.document.getElementById("f5");
   var array = jQuery(form).serializeArray();
   var jsondata = {};

   jQuery.each(array, function() {
     jsondata[this.name] = this.value || '';
   });

   $.ajax({
      url: 'http://localhost:5000/qa/'+jsondata['sessionId']+'/questions/'+jsondata['filter'],
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

