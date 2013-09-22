$(document).ready(function() {
	$("a").click(function(e) {
		if($(this).attr("href") == "") {
			e.preventDefault();
			e.stopPropagation();
		}
	});
//    $("#editnote").submit(function(e) {
//        e.preventDefault();
//        alert($(this).serialize());
//    });
	$(window).scroll(function() {
		var scrollTop = document.documentElement ? document.documentElement.scrollTop : document.body.scrollTop;
		if(scrollTop > 75 || $(document).scrollTop() > 75) {
		    	$("#headerLinks").css("position", "fixed").css("top", "0px");
		} else {
			$("#headerLinks").css("position", "absolute").css("top", "75px");
	    }
	});
	$(".listItem").mouseover(function() {
		$(this).css("background", "#777");
		if($(this).find("h5").text() == "Dir") {
			$(this).find("h5").text("Open")
		} else if($(this).find("h5").text() == "File") {
			$(this).find("h5").text("Download")
		} else if($(this).find("h5").text() == "Notes") {
                        $(this).find("h5").text("Edit")
                }
	}).mouseleave(function() {
		$(this).css("background", "#444");
		if($(this).find("h5").text() == "Open") {
                        $(this).find("h5").text("Dir")
                } else if($(this).find("h5").text() == "Download") {
                        $(this).find("h5").text("File")
                } else if($(this).find("h5").text() == "Edit") {
                        $(this).find("h5").text("Notes")
                }

	});
	
	$(".listItem h3").each(function() {
		if($(this).parent().find("h5").text() == "Dir") {
			$(this).parent().css("border", "#222 solid 2px");
		} else if($(this).parent().parent().find("h5").text() == "Dir") {
                        $(this).parent().parent().css("border", "#222 solid 2px");
                }
//		alert($(this).css("font-size"));
		newFont = parseInt($(this).css("font-size")) - 1;
//		alert(newFont);
		while($(this).height() > 44) {
			temp = $(this).css("font-size");
			temp = temp.substring(0, temp.length - 2);
//			alert(parseFloat(temp) - .2);
//			alert(parseFloat(($(this).css("font-size"))));
			$(this).css("font-size", parseInt(temp) - 1);
//			alert($(this).height());
		}
		$(this).css("font-size",  $(this).css("font-size") - 1);
//                alert($(this).css("font-size"));
	});
	$(".delete").mouseover(function() {
                $(this).css("font-weight", "bold");
        }).mouseleave(function() {
                $(this).css("font-weight", "normal");
        }).click(function() {
		if(confirm("You sure you want to delete " + $(this).attr("name"))) {
			window.location.href = $(this).attr("link");
		}
	});

	$(".done_ren").click(function() {
		if($(this).parent().find(".ren_name").val() == "") {
			alert("enter name");
			return;
		} else {
			window.location.href = $(this).parent().find(".rename").attr("link") + "/" + $(this).parent().find(".ren_name").val() + "/rename"
//			alert($(this).parent().find(".rename").attr("link") + "/" + $(this).parent().find(".ren_name").val() + "/rename")
		}
	});

	$("#calendar").ready(function() {
		var d = new Date();
		date = d.getDate();
		day = d.getDay();
		loadCalendar(d);

	$(".calendar").dblclick(function() {
			if($(this).parent().find(".date_number").text() != "" && $(this).attr("class") == "calendar") {
//				alert("here");
                $(this).attr("id", $(this).parent().find(".date_number").text());
				$("#save_button").css("display", "block");
				$(this).html("<textarea style=\"resize:none;width:100%;height:90%\">" +  $(this).find(".date").html().trim().split("<br>").join("\n") + "</textarea>");
                $(this).css('overflow', 'visible');
				$(this).find("textarea").focus();
				$(this).find("textarea").val($(this).find("textarea").val() + " ");
				$(this).find("textarea").val($(this).find("textarea").val().trim())
			} else if ($(this).attr("class") == "calendar last") {
				prevMonth();
			} else if ($(this).attr("class") == "calendar next") {
				nextMonth();
			}
		});
		
		$("#save_button").click(function() {
//			alert("HI");
			newCal = "";
			$(".calendar").each(function() {
				if($(this).attr("class") != "calendar") {
					return;
				}
				html = $(this).html();
				if(html.indexOf("textarea") !== -1) {
					text = $(this).find("textarea").val();
					text = text.split("\n").join("__n__");
					textAfter = $(this).attr("id") + ":" + text;
					if(text != "") {
						newCal += textAfter + ",,,";
					}
				} else if($(this).find(".date").text().trim() !== "") {
					newCal += $(this).parent().find(".date_number").text() + ":" + $(this).find(".date").html().split("<br>").join("__n__") + ",,,";
				}
			});

			newCal = $("#month_name").attr("ynum") + ":" + $("#month_name").attr("mnum") + ":" +newCal
//			alert($(".month_info p").text() + ":" +newCal);
//			alert(newCal);
			window.location.href = "/calupdate/" + newCal;
		});
		
		$("#next_month").click(function() {
			nextMonth();
		});

		$("#prev_month").click(function() {
            prevMonth();
        });

	});

	var day_names = new Array('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');
	var month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
	var events = "";
	var eventsNext = "";
	var eventsLast = "";

	function nextMonth() {
		var d = new Date($("#month_name").attr("ynum"), parseInt($("#month_name").attr("mnum")) + 1);
		loadCalendar(d);
	}

	function prevMonth() {
                var d = new Date($("#month_name").attr("ynum"), parseInt($("#month_name").attr("mnum")) - 1);
                loadCalendar(d);
        }

	function loadCalendar(d) {
                date = d.getDate();
                day = d.getDay();
		first_day = new Date(d.getFullYear(), d.getMonth(), 1).getDay();
                days_in_month = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
//              alert(new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate());
//              count = 0;
                $("#month_name").text(month_names[d.getMonth()] + "  - " + d.getFullYear());
                $("#month_name").attr("mnum", d.getMonth());
                $("#month_name").attr("ynum", d.getFullYear());
                $(".calendar").each(function(i,j) {
//			alert($(this).parent().html());
                        $(this).html("<span class=\"date\"></span>");
                        $(this).parent().find(".date_number").text('');
                        count = i - first_day + 1;
//                      alert(count);
            if(count > 0 && count <= days_in_month) {
                $(this).parent().find(".date_number").text(i - first_day + 1);
				$(this).attr("class", "calendar");
            } else if (count <= 0) {
				$(this).parent().find(".date_number").text(new Date(d.getFullYear(), d.getMonth(), 0).getDate() + count);
				$(this).attr("class", "calendar last");
			} else if( count > days_in_month) {
				$(this).parent().find(".date_number").text(count - days_in_month);
				$(this).attr("class", "calendar next");
			}

//                      $(this).text((i + date > days_in_month) ? 'hi' : i + date);
                });
                $(".date_name").each(function(i) {
                        $(this).text(day_names[i]);
                });
//              alert($(".week:last").children(":first").children(":first").children(":last").text());
            if($(".week:last").find(".calendar").attr("class") == "calendar next") {
                $(".week:last").css("display", "none");
            } else {
			    $(".week:last").css("display", "table-row");
		    }
//                $(".year_info").each(function(i) {
//                      alert("here");
//                        if($(this).find("h4").text() != d.getFullYear()) {
//                              alert("hi");
//                              $(this).parent().remove();
//                              $(this).parent().html("display", "none");
//                        }
//                });
                $(".month_info").each(function() {
//			$(this).parent().html();
//			alert($(this).parent().find(".year_info h4").text());
//                        if($(this).find("p").text() != d.getMonth()) {
//                              $(this).remove();
                        if($(this).parent().find("h4").text() == d.getFullYear() && $(this).find("p").text() == d.getMonth()) {
//                              $(this).find("p").text(month_names[$(this).find("p").text()]);
//                              alert($(this).find(".day_info").text());
                                events = $(this).find(".day_info").text();
                                events = events.split(",,,");
                                events.pop();
//                              alert(temp.length);
                                for(var num = 0; num < events.length; num++) {
                                        events[num] = events[num].split(":");
                                }
//                              alert(temp);
//                              alert(month_names[$(this).find("p").text()]);
                        } else if($(this).parent().find("h4").text() == d.getFullYear() && $(this).find("p").text() == d.getMonth() + 1) {
				eventsNext = $(this).find(".day_info").text();
				eventsNext = eventsNext.split(",,,");
				eventsNext.pop();
				for (var num = 0; num < eventsNext.length; num++) {
					eventsNext[num] = eventsNext[num].split(":");
				}
			} else if($(this).parent().find("h4").text() == d.getFullYear() && $(this).find("p").text() == d.getMonth() - 1) {
				eventsLast = $(this).find(".day_info").text();
				eventsLast = eventsLast.split(",,,");
				eventsLast.pop();
				for (var num = 0; num < eventsLast.length; num++) {
					eventsLast[num] = eventsLast[num].split(":");
				}
			}
                });
                $(".calendar").each(function() {
			date = $(this).parent().find(".date_number").text();
			if($(this).attr("class") != "calendar") {
				$(this).parent().css("color", "grey");
				if($(this).attr("class") == "calendar next") {
					for( var num = 0; num < eventsNext.length; num++) {
//						alert(eventsNext[num][0] + " " + date);
						if(eventsNext[num][0] == date) {
							
							text = "";
							for(var num2 = 1; num2 < eventsNext[num].length; num2++) {
								text += ":" + eventsNext[num][num2];
							}
							text = text.substr(1).split("__n__").join("<br>");
//							text = text.split("__n__").join("<br>");
							$(this).find(".date").html(text);
						}
					}
				} else if($(this).attr("class") == "calendar last") {
					for( var num = 0; num < eventsLast.length; num++) {
						if(eventsLast[num][0] == date) {
							text = "";
							for(var num2 = 1; num2 < eventsLast[num].length; num2++) {
								text += ":" + eventsLast[num][num2];
							}
							text = text.substr(1).split("__n__").join("<br>");
							$(this).find(".date").html(text);
						}
					}
				}
				return;
			}
			$(this).parent().css("color", "lightgrey");
                        if(date != "") {
                                for(var num = 0; num < events.length; num++) {
                                        if(events[num][0] == date) {
                                                text = "";
                                                for(var num2 = 1; num2 < events[num].length; num2++) {
                                                        text += ":" + events[num][num2];
                                                }
                                                text = text.substr(1).split("__n__").join("<br>");
                                                $(this).find(".date").html(text);
                                        }
                                }
                        }
                });

	}

	$("#dir_name").on("change input", function() {
		if($(this).val() !== "") {
			$("#upload").removeAttr("disabled");
		} else {
			$("#upload").attr("disabled", "disabled");
		}
	});
	
	$(":file").change(function() {
		var file = this.files[0];
		if(file !== undefined) {
			name = file.name;
			size = file.size;
			type = file.type;
			$("#upload_file").removeAttr("disabled");
		} else {
			 $("#upload_file").attr("disabled", "disabled");
		}

	});
	var startTime;
	var prevLoaded = 0;
	var prevTime;
	$("#upload_file").click(function() {
//		alert("here");
		var formData = new FormData($("#add")[0]);
		startTime = new Date().getTime()
		prevTime = new Date().getTime()
		$.ajax({
			url: $(this).attr("url"),
			type: "POST",
			xhr: function() {
				var myXhr = $.ajaxSettings.xhr();
				if(myXhr.upload) {
					myXhr.upload.addEventListener("progress", progressHandling, false);
				}
				return myXhr;
			},
			
			data: formData,
			cache: false,
			contentType: false,
			processData: false,
			success: function() { window.location.href = $(this).attr("url") }
		});
	});
	function progressHandling(e) {
		if(e.lengthComputable) {
			$("#progress").text(truncate("\n" + (e.loaded - prevLoaded) / (new Date().getTime() - prevTime)) + " KB/S - " + truncate((e.loaded / e.total) * 100) + "% - " + truncate(e.loaded/1012) + "/" + truncate(e.total/1012) + " KB");
			prevLoaded = e.loaded;
			prevTime = new Date().getTime();
		}
		function truncate(num) {
			return Math['floor'](num * 100) / 100;
		}
	}

});
