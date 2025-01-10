function formatDate(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = ('0' + (d.getMonth() + 1)).slice(-2);
    const day = ('0' + d.getDate()).slice(-2);
    return `${year}-${month}-${day}`;
}

function toggleTable(tableId, titleId) {
    const table = document.getElementById(tableId);
    const title = document.getElementById(titleId);

    if (table.style.display === "none") {
        table.style.display = "table";
        title.style.display = "block";
    } else {
        table.style.display = "none";
        title.style.display = "none";
    }
}