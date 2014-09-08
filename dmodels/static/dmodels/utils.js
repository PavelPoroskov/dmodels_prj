function isValidValues(_values) {

	function isValedNumber( _str, _min, _max, _strlen ) {

		var res_isValedNumber = true,
			intValue = parseInt(_str, 10 );


		if (isNaN(intValue)) {
			res_isValedNumber = false;
		};

		if (res_isValedNumber) {
			pos_intVal = Math.max( -intValue, intValue ); //?
			norm_strVal = "" + pos_intVal;

			if (_strlen) {
				for ( var i = 0, i_bound = _strlen - norm_strVal.length; i < i_bound; i++ ) {
					norm_strVal = "0" + norm_strVal;
				};
			};
			if (norm_strVal !== _str) {
				res_isValedNumber = false;
			}
		}

		if (res_isValedNumber && _strlen) { // len != 0
			if ( _str.length != _strlen ) {
				res_isValedNumber = false;
			};
		};

		if (res_isValedNumber && (_min != undefined)) {
			if ( ! (_min <= intValue ) ) {
				res_isValedNumber = false;
			}
		};
		if (res_isValedNumber && (_max != undefined) ) {
			if ( ! ( intValue <= _max ) )  {
				res_isValedNumber = false;
			}
		};

		return res_isValedNumber;
	};

	function isValedDate( _strVal ) {
		var res_isValedDate = true;

		var aData = _strVal.split("/");

		res_isValedDate = (aData.length == 3);

		var _YYYY, _mm, _dd;
		if (res_isValedDate) {
			_mm = aData[0];
			_dd = aData[1];
			_YYYY = aData[2];

			res_isValedDate = ( isValedNumber( _YYYY, 0, 9999, 4 ) 
				&& isValedNumber( _mm, 1, 12, 2 ) 
				&& isValedNumber( _dd, 1, 31, 2 ) );
		};

		if (res_isValedDate) {
			var iY = parseInt(_YYYY),
				im = parseInt(_mm) - 1,
				id = parseInt(_dd);

			var d = new Date( iY, im, id );

//			var dY = d.getYear(),
			var dY = d.getFullYear(),			
				dm = d.getMonth(),
				dd = d.getDate();

			res_isValedDate = ( ( dY == iY) && (dm == im) && (dd == id) );
		};

		return res_isValedDate;
	};


	var messages = [];

	var field, type, title, 
		isError, strMessage;
	for (var v=0, v_length=_values.length; v < v_length; v++ ) {
		field = _values[v];

		type = field['type'];
		title = field['title'];

		strVal = field['value'];
		strVal = strVal.trim()

		isError = false;
		strMessage = "";
		if (type == "char") {
			if (strVal == "") {
				isError = true;
				strMessage = "(" + title + " ) is empty.";
			};
		}else if (type == "int") {
			if ( ! isValedNumber( strVal, 1 ) ) {
				isError = true;
				strMessage = "(" + title + " ) is not positive integer number"
			};
		}else if (type == "date") {
			if ( ! isValedDate( strVal ) ) {
				isError = true;
				strMessage = "(" + title + " ) is not valid date"
			};
		};

		field['isError'] = isError;
		field['ErrorMessage'] = strMessage;

		if (isError) {
			messages.push(strMessage);	
		}
	};

	_values['messages'] = messages;

	return (messages.length == 0 );
};

function isValidAndMarkError( _values ) {

	var res = isValidValues( _values );

	var field;
	for (var v=0, v_length=_values.length; v < v_length; v++ ) {
		field = _values[v];
//		if (field['isError']){
//			$(field['el']).addClass('error_field');			
//		};
		$(field['el']).toggleClass('error_field', field['isError'] );
	};

	return res;
};


function drawTable(_data) {

	var elTable, elTBody;	
	var elTR, elTD;

	elTable = document.createElement('table');	

	elTBody = document.createElement('tbody');	
	elTBody.id = "tbody_id";


// header
	var fields = _data.fields;
	var fields_length = fields.length;

	elTR = document.createElement('tr');	
	for (var f=0; f < fields_length; f++) {
		elTD = document.createElement('th'); 
//		elTD.innerHTML = fields[f].title;
		elTD.textContent = fields[f].title;
		
		elTR.appendChild(elTD);	
	};
	elTBody.appendChild(elTR);	
	
	drawTableRows( elTBody, _data.data, fields )

	elTable.appendChild(elTBody);	

	return elTable;	
};

function drawTableRows( elTBody, _rows, _fields ) {

//	var _fields = GLOBAL_STATE['fields']
	var fields_length = _fields.length;

	var elTR, elTD;

	var row;
	for (var r = 0, rows_length = _rows.length; r < rows_length; r++ ) {	
		row = _rows[r];

		elTR = document.createElement('tr');	
		for (var f=0; f < fields_length; f++) {
			elTD = document.createElement('td'); 

//			elTD.innerHTML = row[ f ];
			elTD.textContent = row[ f ];

			elTD.dataset['field'] = f;

			if (_fields[f].id != 'id') {
				elTD.className = _fields[f].type;
			};

			elTR.appendChild(elTD);	
		};
	
		elTBody.appendChild(elTR);	
	};
}

function drawFormAddNew(_data) {

//	console.log('drawAddNew 1');	

	var elForm = document.createElement('form');
	elForm.id = "AddNewForm"

//	elForm.dataset['model'] = _data.model;

	var fieldset = document.createElement('fieldset');
	elForm.appendChild(fieldset);	

	var legend = document.createElement('legend');
//	legend.innerHTML = 'Новая запись';
	legend.textContent = 'Новая запись';
	
	fieldset.appendChild(legend);	


//	console.log('drawAddNew 2');	

//	var fields = _data.structure.fields;
//	var fields = GLOBAL_STATE['fields'];
	var fields = _data.fields;
	var elDiv, elIn, elBr;
	for (var f=0, fields_length = fields.length; f < fields_length; f++) {

//		console.log('drawAddNew circle 1');	
		if (fields[f].id == 'id') {
			continue;
		};

		elDivRow = document.createElement("div");

		elText = document.createTextNode(fields[f]['title'] + ' ');

		elIn = document.createElement("input");
		elIn.setAttribute("type", "text");
		elIn.name = fields[f]['id'];
//		elIn.setAttribute("name", "fields[i].id");
		elIn.className = fields[f]['type'];
		elIn.dataset['title'] = fields[f]['title'];
		elIn.dataset['type'] = fields[f]['type'];

		elDivRow.appendChild(elText)
		elDivRow.appendChild(elIn)

//		elDiv = document.createElement("br");
//		elBr = document.createElement("br");

		fieldset.appendChild(elDivRow);	
//		fieldset.appendChild(elIn);	
//		fieldset.appendChild(elBr);	

//		console.log('drawAddNew circle 2');	
	};
/*
	elIn = document.createElement("input");
	elIn.setAttribute("type", "button");
	elIn.name = "AddButton";
	elIn.value = "Добавить";
	elIn.id = "AddNewButton";
*/
	elIn = document.createElement("input");
	elIn.setAttribute("type", "reset");
	elIn.name = "ResetButton";
	elIn.value = "Отмена";
	elIn.id = "NewRowReset";
	fieldset.appendChild(elIn);	

	elIn = document.createElement("input");
	elIn.setAttribute("type", "submit");
	elIn.name = "AddButton";
	elIn.value = "Добавить";
	elIn.id = "AddNewButton";
	fieldset.appendChild(elIn);	

	return elForm;
};

function draw_RightContent( root, _data) {

//	var root = $("right_content");
	var frag = document.createDocumentFragment();

	var root_div = document.createElement('div');

	var elTable = drawTable(_data);
	var elFormNew = drawFormAddNew(_data);

//	console.log('drawRight mid');	

	root_div.appendChild(elTable);
	root_div.appendChild( document.createElement('p') );
	root_div.appendChild(elFormNew);

	frag.appendChild(root_div)

	root.replaceChild( frag, root.firstChild );
};
