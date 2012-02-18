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
					var info = $("div[id='search'] > div[class='info']");
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
					var list = $("div[id='addwish'] > div[class='list']");
					list.empty();
					var info = $("div[id='addwish'] > div[class='info']");
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
					var info = $("div[id='addwish'] > div[class='info']");
				    info.text(msg);
				    alert(msg)
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
					var list = $("div[id='mywish'] > div[class='list']");
					list.empty();
					var info = $("div[id='mywish'] > div[class='info']");
				    info.text(msg);
				    msg = JSON.parse(msg);
				    if ( msg.status == 200){
				    	var data = msg.root.data
				    	for( var key in data){
				    		var one = data[key]
				    		list.append("<b>"+one['title']+"["+one['expect_price']+"]"+"</b> <button class='opt' href='/my/wish/undo' value="+one['pkey']+"> delete </button><button class='opt' href='/my/wish/buyed' value="+one['pkey']+"> buyed </button><br><input type='text' class='except_price' id='"+one['pkey']+"' /><button class='opt_price' href='/my/wish/price' value="+one['pkey']+"> except </button><br>");
				    	}
				    	
				    	//bindAddClick()
				    	bindMyWishOptClick();
				    	bindMyWishOptClick_price();
				    }
				}
			});
	});
}

function bindMyWishOptClick(){
	$("button[class='opt']").click(function(){
		var tourl = $(this).attr('href');
		var pkey = $(this).attr('value');
		$.ajax({
   				type: "POST",
   				url: tourl,
   				data: "pkey="+pkey,
				success: function(msg){
					var old_msg = msg;
					msg = JSON.parse(msg);
					var info = $("div[id='mywish'] > div[class='info']");
				    info.text(msg);
					alert(old_msg);
				}
			});
	});
}

function loginTest(){
	
	return false;
}
function bindLoginClick(){
	$("form[id='login'] > button").click(function(){
	    var email = $(this).parent().children("input[name='email']").val();
	    var passwd = $(this).parent().children("input[name='password']").val();
	    $.ajax({
   				type: "POST",
   				url: "/user/login",
   				data: "email="+email+"&password="+passwd,
				success: function(msg){
					var old_msg = msg
					msg = JSON.parse(msg);
					if (msg.status == 200){
					    var root = msg.root;
					    $(this).parent().hide()
					}else{
						alert(old_msg);
					}
				}
			});
	});
}


function bindMyWishOptClick_price(){
	$("button[class='opt_price']").click(function(){
		var tourl = $(this).attr('href');
		var pkey = $(this).attr('value');
		var price = $("input[id='"+pkey+"']").val();
		$.ajax({
   				type: "POST",
   				url: tourl,
   				data: "pkey="+pkey+"&price="+price,
				success: function(msg){
					var old_msg = msg;
					msg = JSON.parse(msg);
					var info = $("div[id='mywish'] > div[class='info']");
				    info.text(msg);
					alert(old_msg);
				}
			});
	});
}



function load(){
	$(function () {
			$('.tabs').tabs();
			bindLoginClick();
			bindSearchClick();
			bindSearchWishClick();
			bindMyWishClick();
		})
}