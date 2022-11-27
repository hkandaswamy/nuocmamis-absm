var wholeOrder = "";
var itemOne = "";
var itemTwo = "";
var itemThree = ""; 
var itemFour = "";
var itemFive = "";
function addNewComponent() {
    var tableReference = document.getElementById("tabOne").getElementsByTagName("tbody")[0];
    if (itemOne == "") {
        itemOne = document.getElementById("itemOrderOne").value + "\n   ";
    }
    // Inserts a new row and a cell into the table
    var newRow = tableReference.insertRow();
    var newCell = newRow.insertCell();
    
    // Inputs text into a new row above the text input, empties out text box for more
    // input if user wants
    var inputText = document.getElementById("inputOne").value;
    var newText = document.createTextNode(inputText);

    newCell.appendChild(newText);

    // Prints out the order
    itemOne = itemOne + inputText + "\n   ";
}

function addNewComponentTwo() {
    var tableReference = document.getElementById("tabTwo").getElementsByTagName("tbody")[0];
    if (itemTwo == "") {
        itemTwo = document.getElementById("itemOrderTwo").value + "\n   ";
    }
    // Inserts a new row and a cell into the table
    var newRow = tableReference.insertRow();
    var newCell = newRow.insertCell();
    
    // Inputs text into a new row above the text input, empties out text box for more
    // input if user wants
    var inputText = document.getElementById("inputTwo").value;
    var newText = document.createTextNode(inputText);

    newCell.appendChild(newText);

    // Prints out the order
    itemTwo = itemTwo + inputText + "\n   ";
}

function addNewComponentThree() {
    var tableReference = document.getElementById("tabThree").getElementsByTagName("tbody")[0];
    if (itemThree == "") {
        itemThree = document.getElementById("itemOrderThree").value + "\n   ";
    }
    // Inserts a new row and a cell into the table
    var newRow = tableReference.insertRow();
    var newCell = newRow.insertCell();
    
    // Inputs text into a new row above the text input, empties out text box for more
    // input if user wants
    var inputText = document.getElementById("inputThree").value;
    var newText = document.createTextNode(inputText);

    newCell.appendChild(newText);

    // Prints out the order
    itemThree = itemThree + inputText + "\n   ";
}


function addNewComponentFour() {
    var tableReference = document.getElementById("tabFour").getElementsByTagName("tbody")[0];
    if (itemFour == "") {
        itemFour = document.getElementById("itemOrderFour").value + "\n   ";
    }
    // Inserts a new row and a cell into the table
    var newRow = tableReference.insertRow();
    var newCell = newRow.insertCell();
    
    // Inputs text into a new row above the text input, empties out text box for more
    // input if user wants
    var inputText = document.getElementById("inputFour").value;
    var newText = document.createTextNode(inputText);

    newCell.appendChild(newText);

    // Prints out the order
    itemFour = itemFour + inputText + "\n   ";
}

function addNewComponentFive() {
    var tableReference = document.getElementById("tabFive").getElementsByTagName("tbody")[0];
    if (itemFive == "") {
        itemFive = document.getElementById("itemOrderFive").value + "\n   ";
    }
    // Inserts a new row and a cell into the table
    var newRow = tableReference.insertRow();
    var newCell = newRow.insertCell();
    
    // Inputs text into a new row above the text input, empties out text box for more
    // input if user wants
    var inputText = document.getElementById("inputFive").value;
    var newText = document.createTextNode(inputText);

    newCell.appendChild(newText);

    // Prints out the order
    itemFive = itemFive + inputText + "\n   ";
}

function makeWholeOrderIntoString() {
    wholeOrder = itemOne + "\n";
    if (itemTwo != "") {
        wholeOrder += itemTwo + "\n";
    }
    if (itemThree != "") {
        wholeOrder += itemThree + "\n";
    }
    if (itemFour != "") {
        wholeOrder += itemFour + "\n";
    }
    if (itemFive != "") {
        wholeOrder += itemFive + "\n";
    }
    alert("Order: \n" + wholeOrder);
    return wholeOrder;
}