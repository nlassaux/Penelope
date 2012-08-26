// *****************************************************
//
//		    	Edit assignment function
//     Change and load RequiredFiles in the page
//
// *****************************************************

// These lines are executed when the document has been loaded
$('#addfilebtn').click(function(){
	addrequiredfile('','','','');
});
$('#requiredfilesnb').val($(".requiredfile").length);
$('#id_requirement').change(change_text);
change_text();

// An ajax request to load requiredFilesFields
$.ajax({
	type: "GET",
	url: "/works/" + $('#assignment_id').val() + "/addrequirement/",
	success: function(xml) {
		loadrequiredfiles(xml);
		$('.close').click(function(){
			delete_required(this);
		});
	}
});

// Apply effects when we change value of method select
function change_text() {
	if ($('#id_requirement').val() == 'none') {
		$('#requirementform').hide();
	} else {
		$('#requirementform').show();
	}
};

// Read XML response to build an edit form
function loadrequiredfiles(xml) {
	test = $(xml).find('object').each(function(){
		var id = $(this).attr('pk');
		var name = $(this).find("field[name='name']").text();
		var description = $(this).find("field[name='description']").text();
		var type = $(this).find("field[name='type']").text();
		addrequiredfile(id, name, description, type);
		$('#requiredfilesnb').val($(".requiredfile").length);
	});
}

function delete_required(element) {
	// An ajax request to delete a requiredfile
	$.ajax({
		type: "GET",
		url: "/works/" + $('#assignment_id').val() + "/deleterequirement/",
		data: {id:$(element).attr("id")},
		success: function(xml) {
			window.location.reload();
		}
	});
}

// -----------------------------------------------------
//		    	Add required file function
// -----------------------------------------------------

// Add an empty form with : id, name, description and type fields. Hide id field
function addrequiredfile(id, name, description, type) {
	// the id and name of all fields is dynamically set with that value
	var nextid = $(".requiredfile").length + 1;

	addrequiredfileclass('#requirementform', nextid);
	addclosebtn('.requiredfile:last', id);
	addidfield('.requiredfile:last', id, nextid);
	addnamefield('.requiredfile:last', name, nextid);
	adddescriptionfield('.requiredfile:last', description, nextid);
	addtypefield('.requiredfile:last', type, nextid);

	// set to 'requiredfilenb' field the number of required file as value to be used after POST send
	$('#requiredfilesnb').val($(".requiredfile").length);

	$('.close').click(function(){
		delete_required(this);
	});
};

// Create new <div class='requiredfile'></div> in a parent
function addrequiredfileclass(parent, index){
	$(parent).append("<div class='requiredfile under_panel'></div>");
};

// Add a close button with an 
function addclosebtn(parent, index) {
	var closebtn = "<a class='close' id='" + index + "'>x</a>"
	$(parent).append(closebtn);
};

// Add an id field with a value (content), and an index(index) to add to parent
function addidfield(parent, content, index){
	var idfield = "<input type='text' value='" + content + "' id='requiredfileid" + index + "' name='requiredfileid" + index + "' style='display: none;''/>";
	$(parent).append(idfield);
};

// Add a name field with a value (content), and an index(index) to add to parent
function addnamefield(parent, content, index){
	var namefield = "<label>Name :</label><input type='text' value='" + content + "' name='requiredfilename" + index + "'/>";
	$(parent).append(namefield);
};

// Add a description field with a value (content), and an index(index) to add to parent
function adddescriptionfield(parent, content, index){
	var descriptionfield = "<label>Description :</label><textarea class='input-xlarge' name='requiredfiledescription" + index + "' rows='3'>" + content + "</textarea>";
	$(parent).append(descriptionfield);
};

// Add a type field with a value (content), and an index(index) to add to parent
function addtypefield(parent, content, index){
	var typefield = "<label>Type :</label><select name='requiredfiletype" + index + "'><option value='none'>none</option><option value='tar.gz'>tar.gz</option><option value='pdf'>pdf</option></select>";
	$(parent).append(typefield);
	$('select:last').val(content);

};