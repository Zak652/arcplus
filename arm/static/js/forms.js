//Asset capture form dropdown cascading

// $(function () {
// 	var typesdropdown = {
// 		category: document.getElementsByName("category"),
// 		assettypes: document.getElementsByName("_type")
// 	};
// 	// function to call XHR and update typesdropdown
// 	function updateassettypes() {
// 		var category = typesdropdown.category.val();
// 		typesdropdown.assettypes.attr('disabled', 'disabled');
// 		console.log(category);
// 		if (category.length) {
// 			typesdropdown.assettypes.empty();
// 			$.getJSON("{{ url_for('/register/add_asset') }}", { category: category }, function (data) {
// 				console.log(data);
// 				data.forEach(function (item) {
// 					typesdropdown.assettypes.append($('<option>', {
// 						value: item.id,
// 						text: item.name
// 					}));
// 				});
// 				typesdropdown.assettypes.removeAttr('disabled');
// 			});
// 		}
// 	}
// 	// event listener to assettype dropdown change
// 	typesdropdown.category.on('change', function () {
// 		updateassettypes();
// 	});
// });


var category_select = document.getElementsByName('category')[0];
var type_select = document.getElementsByName('_type')[0];
var model_select = document.getElementsByName('_model')[0];

category_select.onchange = function() {
	category = category_select.value;
	
	fetch('/register/add_asset_types_dropdown/' + category).then(function(response){
		response.json().then(function(data) {
			OptionHTML = '';
			
			for (let _type of data.asset_types) {
				OptionHTML += '<option value="' + _type.id + '">' +  _type.type_name + '</option>';
			}

			type_select.innerHTML = OptionHTML;

		});
	});
}

type_select.onchange = function() {
	_type = type_select.value;
	
	fetch('/register/add_asset_models_dropdown/' + _type).then(function(response){
		response.json().then(function(data) {
			OptionHTML = '';
			
			for (let _model of data.asset_models) {
				OptionHTML += '<option value="' + _model.id + '">' +  _model.model_name + '</option>';
			}

			model_select.innerHTML = OptionHTML;

		});
	});
}