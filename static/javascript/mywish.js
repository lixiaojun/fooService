function bindClick(){
	$("button[name='mywish']").click(function(){
	    var name = $(this).attr("name");
	    $.ajax({
   				type: "POST",
   				url: "/my/wish",
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
				    		list.append("<b>"+one['title']+"</b> <button class='opt' href='/my/wish/delete' value="+one['pkey']+"> delete </button><button class='opt' href='/my/wish/buyed' value="+one['pkey']+"> buyed </button><br>");
				    	}
				    	
				    	//bindAddClick()
				    }
				}
			});
	});
}

function load(){
	$(document).ready(function(){
	    bindClick()
	});
}