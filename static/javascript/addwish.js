function bindSearchClick(){
	$("button[name=title]").click(function(){
	    var name = $(this).attr("name");
	    var val = $("input[name='"+name+"']").val();
	    if(val){
	    	$.ajax({
   				type: "POST",
   				url: "/search/product/"+name,
   				data: "search="+val,
				success: function(msg){
					var list = $("div[id='list']");
					list.empty();
					var info = $("div[id='info']");
				    info.text(msg);
				    msg = JSON.parse(msg);
				    if ( msg.status == 200){
				    	var data = msg.root.data
				    	for( var key in data){
				    		var one = data[key]
				    		list.append("<b>"+one['title']+"</b> <button class='add' href='/my/wish/follow' value="+one['pkey']+"> Add </button><br>");
				    	}
				    	
				    	bindAddClick()
				    }
				}
			});
		}else{
			alert("Please Enter Some text.");
		}
	});
}

function bindAddClick(){
	$("button[class='add']").click(function(){
		var href= $(this).attr('href');
		var pkey = $(this).attr('value');
		$.ajax({
   				type: "POST",
   				url: href,
   				data: "pkey="+pkey,
				success: function(msg){
					var info = $("div[id='info']");
				    info.text(msg);
				}
			});
	});
}

function load(){
	$(document).ready(function(){
	    bindSearchClick()
	});
}