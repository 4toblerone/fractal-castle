$(document).ready(
 function(){

var newproject = $('#newproject');
var admindata = $('#admindata');
var edtpro =$()

$('#newproject').hide();
$("#admindata").hide();
$('#upload').hide();
$('#edtpro').hide();
$("#progressbar").progressbar();
$("#progressbar").hide();
$("#indexprojects").hide();
$("#sortproject").sortable()
$( "#sortable" ).sortable(); 
$( "#sortable" ).disableSelection();
$("#project").prepend("<option value='' selected='selected'></option>");

$("#changedata").click(function(){
  alert("nesto se desava");
$("#admindata").toggle('slow');

});
$("#btnnewproject").click(function(){
  $('#newproject').toggle('slow');
});
$("#uploadphoto").click(function(){
  $('#upload').toggle('slow');
});

$("#editproject").click(function(){
  $('#edtpro').toggle('slow');
  $("#editproject").fadeTo(0, 1);
});
// when project is selected from dropdown list
// it fills html input with project properties data
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
    $('#ispublished').prop('checked' , data.ispublished)
  }
});
});

//creates new project
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
            //put result in some awesome DIV
        }
        else{
        $("#project").append("<option value='"+data.projectkey+"'>"+data.projectname+"</option>");
        alert(data.result+" ," + data.message)
      }
    }
  });
});


var updateids = function(){
  $('#sortable li').each(function(n){
    $(this).attr("id" , n+1);
    $(this).children('.checkbox').attr("value" , n+1)
  });
};

//saves edited data of certain project
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
   "projectkey": $("#projectkey").text(),
   "publish": $("#ispublished").is(':checked')},
   success: function (data){
    updateids();
   }
 });

});

//returns list of projects shown on index/project page
$("#editindex").click(function(){
  alert("pozvao je edit");                                                      
  $('#sortproject').empty();
  $.ajax({
    type: "GET",
    url: "returnindex",
    contentType: "application/json; charset=utf-8",
    success: function(data){
      $("#sortproject").append(data.projectlist);
      }
  });
  $("#indexprojects").toggle('slow');
});

//saves new order of projects which are shown on index/project page
$("#btnsaveeditindex").click(function(){
  alert("sejv je pokusan");
  $.ajax({
    type: "GET" ,
    url: "/saveeditedindex" ,
    contentType : "application/json; charset=utf-8",
    data : { "newprorder" : $("#sortproject").sortable('toArray').toString()},
    success: function(data){
      $("#sortproject li").each(function(n){
      $(this).attr("id" , n+1);
      });
    }
  });

});

//saves changed user data
$('#saveuser').click(function(){
  $.ajax({
    type: "GET",
    url: '/saveediteduser',
    contentType: "application/json; charset=utf-8",
    data: {"newusername": $('#newusername').val(),
            "oldpass": $('#oldpass').val(),
              "newpass": $('#newpass').val(),
                "newemail" : $('#newemail')},
    success: function(data){
      //clear all fields and show message about success of the operation
    }
  });
});


});
