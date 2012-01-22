function bindClick(){
	$("button").click(function(){
	    var name = $(this).attr("name");
	    var val = $("input[name='"+name+"']").val();
	    if(val){
	    	$.ajax({
   				type: "POST",
   				url: "/search/product/"+name,
   				data: "search="+val,
				success: function(msg){
					var info = $("div[id='info']");
				    info.text(msg);
				}
			});
		}else{
			alert("Please Enter Some text.");
		}
	});
}

function load(){
	$(document).ready(function(){
	    bindClick()
	});
}