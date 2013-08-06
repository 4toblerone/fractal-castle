$(document).ready(
 function(){
    $("#contact").on('click', function(event){
    	$("#contact-content").fadeToggle();
    	event.preventDefault();
    });
});