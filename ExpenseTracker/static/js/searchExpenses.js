const searchField = document.querySelector("#searchField");
const appTable = document.querySelector('.app-table')
const paginationContainer = document.querySelector('.pagination-container')
const tableBody = document.querySelector('.table-body')
const tableOutput = document.querySelector(".table-output");
//hide search table by default
tableOutput.style.display = "none";
searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display='none';
    console.log("search value", searchValue);
    tableBody.innerHTML=""; 
    fetch("/search-expenses/", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
          appTable.style.display='none';
          tableOutput.style.display='block';
         
        if (data.length === 0) {
            tableOutput.innerHTML="No results found";
        }else{
            data.forEach((item) => {
                tableBody.innerHTML+=`
                <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.date}</td>
                <td>${item.description}</td>
                
                
                </tr>
                
                `

            })
           
        }
      });
  }else{
    appTable.style.display='block';
    paginationContainer.style.display='block';
    tableOutput.style.display='none';

  }
});
