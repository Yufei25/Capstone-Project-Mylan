$(document).ready(function () {
    $('#contracts_list').DataTable();
});


$(document).on('click', '.confirm-delete', function () {
    return confirm('Are you sure you want to delete all contracts?');
})



