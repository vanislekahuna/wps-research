var table = document.getElementById("dataTable");  // table and button elements
var tbody = table.getElementsByTagName("tbody")[0];
var addRowBtn = document.getElementById("addRowBtn");
var listDataBtn = document.getElementById("listData");

var localStorageKey = "tableData";  // define localStorage key
let tableData = JSON.parse(localStorage.getItem(localStorageKey)) || [];  // load table data from localStorage
console.log(tableData)
//renderTableRows();  // render table rows from loaded data

addRowBtn.addEventListener("click", addRow); // add event listeners
addColBtn.addEventListener("click", addCol);
clearBtn.addEventListener("click", clearData);
listDataBtn.addEventListener("click", listData);
renderRowsBtn.addEventListener("click", renderTableRows);
var n_rows = parseInt(localStorage.getItem("n_rows"))
var n_cols = parseInt(localStorage.getItem("n_cols"))
if(!n_rows) n_rows = 0;
if(!n_cols) n_cols = 1;

// titles for new colums
var col_titles = JSON.parse(localStorage.getItem("col_titles")) || [];
if(!col_titles) col_titles = []; // start with empty array

renderTableRows();  // render table rows from loaded data


// probably need to save number of rows and columns 
function renderTableRows(){
  table = document.getElementById("dataTable");
  table.innerHTML = "<thead><tr><th>Exclude</th><th>Name</th></tr><thead>"
  table = document.getElementById("dataTable");
  
  var headerRow = table.rows[0];  // add a new table header cell
  while(table.rows[0].cells.length < n_cols + 1){
    var newHeaderCell = document.createElement("th");
    var new_col_title = col_titles[table.rows[0].cells.length - 2]; 
    newHeaderCell.textContent = new_col_title;
    headerRow.appendChild(newHeaderCell);
  }

  for (let i = 0; i < tableData.length; i++){
    const row = table.insertRow(-1);   // render table rows from loaded data
    const checkboxCell = row.insertCell(0)
    const nameCell = row.insertCell(1)
    checkboxCell.innerHTML = `<input type="checkbox" ${tableData[i].isChecked? "checked": ""} onchange="updateTableData(${i}, 'isChecked', this.checked)">`
    nameCell.innerHTML = `<input type="text" value="${tableData[i].name}" oninput="updateTableData(${i}, 'name', this.value)">`

    // render additional cols
    for(let j = 2; j <= n_cols; j++){
      // console.log(i, j)
      var nameCells = row.insertCell(j)
      var nameData = tableData[i]["name" + j.toString()]
      nameCells.innerHTML = `<input type="text" value="${nameData}" oninput="updateTableData(${i}, 'name${j}', this.value)">`
    }
  }
}

function addRow(){
  const newRowData = {isChecked: false, name: ""}; tableData.push(newRowData);  // add a row to the table
  const rowIndex = tableData.length - 1;
  const row = table.insertRow(-1);
  const checkboxCell = row.insertCell(0);
  const nameCell = row.insertCell(1);
  checkboxCell.innerHTML = `<input type="checkbox" ${tableData[rowIndex].isChecked ? "checked" : ""} onchange="updateTableData(${rowIndex}, 'isChecked', this.checked)">`;
  nameCell.innerHTML = `<input type="text" value="" oninput="updateTableData(${rowIndex}, 'name', this.value)">`;

  n_rows = n_rows + 1
  saveTableData();  // save updated table data to localStorage

  // make sure ragged rows are topped up!!!
}

function addCol(){
  var headerRow = table.rows[0];  // add a new table header cell
  var newHeaderCell = document.createElement("th"); 
  var new_col_title = "new col";
  newHeaderCell.textContent = new_col_title;
  col_titles.push(new_col_title);
  headerRow.appendChild(newHeaderCell);

  // iterate over the non-header rows
  for(var i = 1; i <= tableData.length; i++){
    var new_cell = table.rows[i].insertCell(-1);
    var rowIndex = tableData.length - 1;
    new_cell.innerHTML = `<input type="text" value="new" oninput="updateTableData(${rowIndex}, 'name', this.value)">`;
    tableData[i-1]["name" + (n_cols +1).toString()]= "stuff";
  }
  n_cols = n_cols + 1
  renderTableRows();
  saveTableData();
 
  // make sure ragged cols are topped up!!!
}

function updateTableData(rowIndex, property, value){
  tableData[rowIndex][property] = value;  // update table data
  saveTableData();  // save to localStorage
}

function saveTableData(){
  console.log(tableData)
  localStorage.setItem(localStorageKey, JSON.stringify(tableData));  // save table data to localStorage
  localStorage.setItem("n_rows", n_rows.toString())
  localStorage.setItem("n_cols", n_cols.toString())
  localStorage.setItem("col_titles", JSON.stringify(col_titles));
}

function listData(){
  var tableDataArray = [];
  var tableRows = table.getElementsByTagName("tr");   // list table data to console
  for(var i = 1; i < tableRows.length; i++){
    var rowData = tableRows[i].getElementsByTagName("td")[1].getElementsByTagName("input")[0].value;  // get value of second cell
    tableDataArray.push(rowData);
  }
  console.log(tableDataArray);
}

function clearData(){
  n_rows = 0
  n_cols = 0
  tableData = null;
  localStorage.removeItem("n_rows")
  localStorage.removeItem("n_cols")
  localStorage.removeItem("col_titles")
  localStorage.removeItem(localStorageKey);
  location.reload()
}
