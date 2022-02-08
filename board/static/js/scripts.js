"use strict";

function view_vid(post) {

	let vid_tag = document.getElementById("vid_"+post);
	if (vid_tag.className == "thumb_vid") {
		vid_tag.controls = true;
		vid_tag.className = "full_vid"
	    vid_tag.height = vid_tag.videoHeight;
	    vid_tag.width = vid_tag.videoWidth;
	    vid_tag.onclick = 'close_video(post)';
	}
	else if (vid_tag.className == "full_vid") {
		close_video(vid_tag, post);
	}

}

function close_video(vid_tag, post) {

	vid_tag.pause();
	vid_tag.controls = false;
	vid_tag.height = 150;
	vid_tag.width = 150;
	vid_tag.className = "thumb_vid";

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

