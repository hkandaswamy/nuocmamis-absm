var wholeOrder = "";

function addNewComponent() {
    var tableReference = document.getElementById("tab").getElementsByTagName("tbody")[0];
    if (wholeOrder == "") {
        wholeOrder = document.getElementById("itemOrder").value + "\n   ";
    }
    // Inserts a new row and a cell into the table
    var newRow = tableReference.insertRow();
    var newCell = newRow.insertCell();
    
    // Inputs text into a new row above the text input, empties out text box for more
    // input if user wants
    var inputText = document.getElementById("input").value;
    var newText = document.createTextNode(inputText);

    newCell.appendChild(newText);

    // Prints out the order
    wholeOrder = wholeOrder + inputText + "\n   ";
}

function makeWholeOrderIntoString() {
    alert("Order: \n" + wholeOrder);
    return wholeOrder;
}