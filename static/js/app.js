$(document).ready(function() {
  $('#productId').on('input', function() {
    var productId = $(this).val();
    $.ajax({
      type: "POST",
      url: "/get_part_id",
      data: {
        productId: productId
      },
      success: function(response) {
        $('#part_id').val(response.part_id);
        $('#area').val(response.area);
      }
    });
  });

  $('#vendor_id').on('input', function() {
    var vendorId = $(this).val();
    $.ajax({
      type: "POST",
      url: "/get_vend_id",
      data: {
        vendor_id: vendorId
      },
      success: function(response) {
        $('#vendor_address').val(response.vendor_address);
        $('#vendor_phn').val(response.vendor_phn);
      }
    });
  });
  $(document).ready(function() {
  $('#location_id').change(function() {
    var location_id = $(this).val();
    $.ajax({
      url: '/get_remaining_area',
      data: {'location_id': location_id},
      dataType: 'json',
      success: function(data) {
        $('#remaining_area').val(data['remaining_area']);
      }
    });
  });
});
    $('#location_id').on('input', function() {
    var locationId = $(this).val();
    $.ajax({
      type: "POST",
      url: "/get_location_area",
      data: {
        location_id: locationId
      },
      success: function(response) {
        $('#location_area').val(response.location_area);
      }
    });
  });


  $('#operationperson_id').on('input', function() {
    var personId = $(this).val();
    $.ajax({
      type: "POST",
      url: "/get_person_id",
      data: {
        operationperson_id: personId
      },
      success: function(response) {
        $('#operationperson_phn').val(response.operationperson_phn);
      }
    });
  });

$(document).ready(function() {
  $('#submit-button').click(function(event) {
    event.preventDefault();

    var quantity = $('#quantity-input').val();

    $.ajax({
      url: '/inwarding/',
      type: 'POST',
      data: $('form').serialize(),
      success: function(response) {
        alert('Inwarding added successfully.');
        location.reload();
      },
      error: function(xhr, status, error) {
        alert(xhr.responseText);
      }
    });
  });
});



});
