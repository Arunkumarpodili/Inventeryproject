$('#movements_from').submit(function(event) {
    event.preventDefault(); // prevent the form from submitting
    var quantity = $('#quantity').val();
    var productId = $('select[name="productId"]').val();
    var fromValue = $('#fromLocation').val();
    var toValue = $('#toLocation').val();
    var location_id = $('input[name="location_id"]').val();

    // Check if quantity is valid
    if (quantity <= 0) {
        alert('Please enter a positive value for quantity.');
        return false;
    }
    if (fromValue === toValue) {
        alert('Both locations cannot be the same.');
        $('#toLocation').val('');
        return false;
    }
    if (fromValue === '' || toValue === '') {
        alert('Please fill out both fields.');
        return false;
    }

    $.ajax({
        type: 'POST', // Change the request method to POST
        url: '/check_quantity/',
        data: { quantity: quantity, productId: productId, location_id: location_id, fromLocation: fromValue }, // Add fromLocation to the data object
        success: function(response) {
            if (response == 'true') {
                // if quantity is valid, submit the form
                $('#movements_from').off('submit').submit();
            } else if (response == 'false') {
                // if inwarding_entry is None, display a pop-up or alert message
                console.log('Please add products to inwarding.');
                alert('Please add products to inwarding.');
                return false;
            } else {
                // if quantity is not valid, display a pop-up or alert message
                console.log('Insufficient quantity in inwarding.');
                alert('Please add products to inwarding.');
                return false;
            }
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });
});
