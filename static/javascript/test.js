function bindSearchClick(){
	$("div[id='search'] > button").click(function(){
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

function bindSearchWishClick(){
	$("div[id='addwish'] > button").click(function(){
	    var name = $(this).attr("name");
	    var val = $("div[id='addwish'] > input[name='"+name+"']").val();
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
				    	
				    	bindAddWishClick()
				    }
				}
			});
		}else{
			alert("Please Enter Some text.");
		}
	});
}

function bindAddWishClick(){
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

function bindMyWishClick(){
	$("div[id='mywish'] > button[name='mywish']").click(function(){
	    var name = $(this).attr("name");
	    $.ajax({
   				type: "POST",
   				url: "/my/wish",
				success: function(msg){
					var list = $("div[id='mywish'] >div[id='list']");
					list.empty();
					var info = $("div[id='mywish'] >div[id='info']");
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
	$(function () {
			$('.tabs').tabs();
			bindSearchClick();
			bindSearchWishClick();
			bindMyWishClick();
		})
}