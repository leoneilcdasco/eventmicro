(function($) {

    // ==============================================================
    // SET target event id
    // ==============================================================
    $(document).on('click', '.webinar_btn', function (e) {
        var event_id = $(this).data('event-id');
        $('#event_id').val(event_id);
    });

    // ==============================================================
    // Check if string is empty
    // ==============================================================
    function isEmpty(str) {
        return str == null || !str.trim().length;
    }

    // ==============================================================
    // Validates User input
    // ==============================================================            
    function check_input(){
        var value = $("[name='first_name']").val();
        if (isEmpty(value)) return false;

        var value = $("[name='last_name']").val();
        if (isEmpty(value)) return false;

        var email = $("[name='email']").val();
        if (isEmpty(email)) return false;

        var email2 = $("[name='email_verify']").val();
        if (isEmpty(email2)) return false;

        var value = $("[name='phone']").val();
        if (isEmpty(value)) return false;

        var value = $("[name='dob']").val();
        if (isEmpty(value)) return false;

        if (email !== email2) return false;
        return true;
    }

    // ==============================================================
    // Reset input form
    // ==============================================================    
    $('#reg-dialog').on('show.bs.modal', function (e) {
        $('#reg_form')[0].reset();
    })
   
    // ==============================================================
    // POST registration dialog 
    // ==============================================================
    $(document).on('click', '#register_btn', function (e) {
        e.stopPropagation()

        formData = $('#reg_form').serializeArray();

        if (!check_input()) {
            alert('Please provide all required fields or valid input!')
            return false;
        }
        
        var has_error = false;
        $.ajax({
            type: 'POST',
            url: '/register',
            async: false,
            data: formData,
            sucess: function(data){
                console.log('Success >>> ' + data)
            },
            error: function(data){
                has_error = true;
                console.log('Error >>> ' + data)
                alert('Registration failed, please contact system admin!');
            },
            complete: function(data){
                // Show FINISH dialog here
                if (!has_error) {
                   $('#reg-dialog').modal('hide');
                   $('#success-dialog').modal('show');
                } 
            }	
          });
    });

})(jQuery);