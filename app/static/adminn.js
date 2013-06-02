$(document).ready(
 function(){
 			
$('#newproject').hide();
$("#progressbar").progressbar();
$("#progressbar").hide();

$("#sortproject").sortable()
$( "#sortable" ).sortable(); 
$( "#sortable" ).disableSelection();
$("#project").prepend("<option value='' selected='selected'></option>");

$("#btnnewproject").click(function(){
  $('#newproject').toggle('slow');
});

var updateids = function(){
  $('#sortable li').each(function(n){
    $(this).attr("id" , n+1);
  });
};

$("#btncreate").click(function(){

  $.ajax({
    type: "GET",
    url: "/createnewproject",
    contentType: "application/json; charset=utf-8",
    data: {"projectname": $("#newprname").val(), 
            "description" : $("#newprdescription").val(),
              "publish" : $("#publish").is(':checked')},
    success: function(data){
        if(data.result==false){
            alert("vec postoji")
            //stavi data.result u neki lep DIV 
        }
        else{
        $("#project").append("<option value='"+data.projectkey+"'>"+data.projectname+"</option>");
        alert(data.result+" ," + data.message)
      }
    }
  });
});

$("#editindex").click(function(){
  alert("pozvao je edit")
  $('#sortproject').empty();
  $.ajax({
    type: "GET",
    url: "returnindex",
    contentType: "application/json; charset=utf-8",
    success: function(data){
      $("#sortproject").append(data.projectlist);
      }
  });

});


$('#project').change(function(){
  $('#sortable').empty();
  var choosenpr = $(this).val();
  $.ajax({
   type: "GET",
   url: "/returnproject",
   contentType: "application/json; charset=utf-8",
   data: {'projectkey' : choosenpr},
   success: function(data){
    $("#sortable").append(data.listitems);
    $("#projectname").val(data.projectname);
    $('#description').val(data.prdescription);
    $('#projectkey').html(data.projectkey)
    $('#hiddenkey').val(data.projectkey)

  }
});
});

$("#btnedit").click(function(){
  var selected = new Array();
  $('ul li input:checked').each(function() {
    selected.push($(this).attr('value'));
  });
  alert(selected);
  //selected = 5;
  $.ajax({
   type: "GET",
   url: "/saveeditedproject",
   contentType: "application/json; charset=utf-8",
   data: {"neworder":  $( "#sortable" ).sortable('toArray').toString(),
   "newname" : $("#projectname").val(),
   "newdescription" : $("#description").val(),
   "photostodelete": selected.toString(),
   "projectkey": $("#projectkey").text()},
   success: function (data){
    updateids();
   }
 });

});



$("#btnsaveeditindex").click(function(){
  $.ajax({
    type: "GET" ,
    url: "/saveeditedindex" ,
    contentType : "application/json; charset=utf-8",
    data : { "newprorder" : $("#sortproject").sortable('toArray').toString()}
  });

});




});
