function PutData (e) {
    e.preventDefault();
    var butNum = document.getElementById('addField').value
    var name_id = parseInt(butNum, 10);

    var name = document.getElementById("name").value;
    var type = document.getElementById("type").value;
    var tag = document.getElementById("tag").value;


    var newRow = document.createElement("tr");
    newRow.setAttribute("id", name_id)

    var newCellName = document.createElement("td");
    var tBoxName = document.createElement('input');
    tBoxName.setAttribute('type', 'text');
    tBoxName.setAttribute('value', name);
    tBoxName.setAttribute('name', 'name'+name_id);
    newCellName.appendChild(tBoxName);

    var newCellTag = document.createElement("td");
    var tBoxTag = document.createElement("input");
    tBoxTag.setAttribute('type', 'text');
    tBoxTag.setAttribute('value', tag);
    tBoxTag.setAttribute('name', 'tag'+name_id);
    newCellTag.appendChild(tBoxTag)

    var newCellType = document.createElement("td");
    var tBoxType = document.createElement("input");
    tBoxType.setAttribute('type', 'text');
    tBoxType.setAttribute('value', type);
    tBoxType.setAttribute('name', 'type'+name_id);
    newCellType.appendChild(tBoxType)

    var newDelete = document.createElement('td')
    var boxDelete = document.createElement("a")
    var boxDelete1 = document.createElement('h5')
    boxDelete1.setAttribute("color", 'blue')
    boxDelete1.setAttribute("value", name_id)
    boxDelete1.setAttribute("id", name_id)
    boxDelete1.setAttribute("onclick", "DeleteColumn(this);")
    boxDelete1.innerHTML = "Удалить"
    boxDelete.appendChild(boxDelete1)
    newDelete.appendChild(boxDelete)

    newRow.append(newCellName, newCellType, newCellTag, newDelete);
    document.getElementById("rows").appendChild(newRow);
    document.getElementById("name").value = '';
    document.getElementById("tag").value = '';
    name_id = name_id + 1
    document.getElementById('addField').value = name_id
    document.getElementById('add_number').value = name_id

    console.log(document.getElementById('add_number'))
}
function DeleteColumn(btn) {
    var row = btn.parentNode.parentNode;
    row.parentNode.remove(row);

}