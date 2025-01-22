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

    table.classList.toggle('hidden');
    title.classList.toggle('hidden');
}