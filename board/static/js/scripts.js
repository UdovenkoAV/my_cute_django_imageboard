"use strict";

function close_vid(post) {
	let video_tag = document.getElementById("vid_"+post);
	let thumb_tag = document.createElement('img');
	let close_button = document.getElementById("close_b_"+post);
	thumb_tag.className = "thumb_vid";
	thumb_tag.id = "vid_"+post;
	thumb_tag.src = thumb_tag.dataset.thumbSrc = video_tag.dataset.thumbSrc;
	thumb_tag.dataset.fullSrc = video_tag.dataset.fullSrc;
	video_tag.replaceWith(thumb_tag);
	close_button.remove();
}

function view_vid(post) {

	if (document.getElementById("vid_"+post).className == "thumb_vid"){
		let thumb_tag = document.getElementById("vid_"+post);
	    let video_tag = document.createElement("video");
		let close_batton = document.createElement('a');
		close_batton.href = "javascript:close_vid("+post+")";
		close_batton.id = "close_b_"+post
		close_batton.innerText = '[CLOSE X]';
	    video_tag.src = video_tag.dataset.fullSrc = thumb_tag.dataset.fullSrc;
		video_tag.dataset.thumbSrc = thumb_tag.dataset.thumbSrc;
	    video_tag.id = "vid_"+post;
	    video_tag.controls = true;
		thumb_tag.replaceWith(video_tag);
		video_tag.before(close_batton);
	}

}


function view_img(post) {

    let img_tag = document.getElementById("img_"+post);
	if (img_tag.className == "thumb_img") {
		img_tag.src = img_tag.dataset.fullSrc;
		img_tag.className = "full_img";
	}
	else if  (img_tag.className == "full_img"){
		img_tag.src = img_tag.dataset.thumbSrc;
		img_tag.className = "thumb_img";
	}

}

function insert(text) {

	let text_form = document.getElementById("id_body");
	if (text_form.value) {
		text_form.value += " " + text;
	}
	else {
		text_form.value += text;
	}
	text_form.focus();
}

function highlight(post) {

	let cells=document.getElementsByTagName("div");
	for(var i=0;i<cells.length;i++) if(cells[i].className=="highlight") cells[i].className="post";

	let reply=document.getElementById("post_"+post);
	if(reply)
	{
		reply.className="highlight";
		return false;

	}
	return true;

}


window.onload = function() {

	let match = ''
	if(match=/#i([0-9]+)/.exec(document.location.toString())){
		insert(">>"+match[1]);
	}

	if(match=/#([0-9]+)/.exec(document.location.toString())){
		highlight(match[1]);
	}
}

