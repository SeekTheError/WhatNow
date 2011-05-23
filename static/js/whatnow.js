function submitCallback(){
val=$("#key").val();
console.log(val);
$("#navigation").removeClass('hidden');
$("#navigation").html("Viewing Topic: <b>"+val+"</b>");
$("#navigation").attr("topic",val);
}




