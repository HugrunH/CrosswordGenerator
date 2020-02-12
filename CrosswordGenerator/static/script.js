// Styling the grid
function GetCellValues() {
    var table = document.getElementById('gameBoard');
    // Iterating through the grid and selecting each cell
    for (var row = 0; row < table.rows.length; row++) {
        for (var cell = 0; cell < table.rows[row].cells.length; cell++) {
            // If cell has value 0 it should be a shaded square
            if((table.rows[row].cells[cell].innerText) == 0) {
                table.rows[row].cells[cell].style.backgroundColor = "black";
            }
            // Otherwise the square should be blank
            else {
                table.rows[row].cells[cell].style.backgroundColor = "white";
            }
            // Need to clear the values (0 and 1) from the cells
            clear(table.rows[row].cells[cell]);
        }
    }
}

/* 
 * Here we tried to implement a function to populate the grid
 * with the solution but proved to be too hard and ultimately not worth it
 */

// function showSolution() {
//     var solution = $('.sol');
//     var parsedSolution = [];
//     console.log(solution);
//     var table = document.getElementById('gameBoard');
//     for(var i = 0; i < solution.length; i++) {
//         console.log(solution[i].textContent);
//         parsedSolution.push(solution[i].textContent)//.substring(3));
//     }
//     console.log(parsedSolution);
//     for (var row = 0; row < table.rows.length; row++) {
//         for(var cell = 0; cell < table.rows[row].cells.length; cell++) {
//             if(table.children[row].children[row].children[cell].style.backgroundColor == 'white') {
//                 if(parsedSolution[row][0] == 'H') {
//                     console.log(table.children[row].children[row].children[cell].textContent);
//                     console.log(parsedSolution[row].substring(3)[cell]);
//                     table.children[row].children[row].children[cell].textContent = parsedSolution[row].substring(3)[cell];
//                 }
//             }
//         }
//     }

//     for(var i = 0; i < parsedSolution[row].substring(3).length; i++) {
//         table.children[0].children[0].children[row].textContent = parsedSolution[row].substring(3)[i];
//     }
// }

// Button for showing the solution
$('.show-sol').on('click', () => {
    $('#solution-list').toggleClass('solution');
});

// Clears the content of the cells
function clear(cell) {
    cell.innerText = '';        
}

// Mark the cells with the appropriate hint numbers
function markCells() {
    var table = document.getElementById('gameBoard');
    var cells = $('.hint_pos');
    var positions = [];
    for(var i = 0; i < cells.length; i++) {
        var a = (cells[i].innerText[2]); // Parse the second letter of the cell, the column index
        var b = (cells[i].innerText[7]); // Parse the seventh letter of the cell, the row index
        // Iterate through the grid selecting cells which words start from
        for(var row = 0, n = table.rows.length; row < n; row++) {
            for(var cell = 0; cell < table.rows[row].cells.length; cell++) {
                // Collect all coordinates of in an array
                positions.push(table.rows[b].cells[a])
                break;
            }
            break;
        }
    }

    /* 
     * As a result of clearing the cells the div's
     * that held the cell values were deleted from the DOM
     * so we need to create new div nodes to hold the new values
     */  
    for(var i = 0; i < positions.length; i++) {
        var node = document.createElement("DIV");
        node.className = 'numbers';
        var textNode = document.createTextNode(i + 1);
        node.appendChild(textNode);
        positions[i].appendChild(node);
    }
}

/* 
 * Important to clear the values first
 * before creating the new values
 */

GetCellValues();
markCells();


// Open the sidebar
function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}
  
// Close the navbar
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
}