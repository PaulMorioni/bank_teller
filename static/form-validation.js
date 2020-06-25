$(function() {

    //names will reflect python conventions as name defaults are set by WTForms 

    $("form[name='buyForm']").validate({
        rules: {

             buy_from_id : 'required',
             amount : 'required'

        },

    messages: {
        buy_from_id: "Please enter ID",
        amount: 'Please enter amount'

    },

    submitHandler: function(form) {
        form.submit();
      }


    });


    $("form[name='sellForm']").validate({
        rules: {

            sell_to_id : 'required',
            amount : 'required'

        },

    messages: {
        sell_to_id: "Please enter ID",
        amount: 'Please enter amount'

    },
    

    submitHandler: function(form) {
        form.submit();
    }


    });

    $("form[name='newCustomerForm']").validate({

        rules:{
            name: 'required',
            dob: 'required',
            ssn: 'required'
        },

        messages:{

        },

        submitHandler: function(form) {
            form.submit();
        }
    
    });

    $("form[name='newAccountForm']").validate({

        rules:{
            account_number: 'required',
            primary_ssn: 'required',
            bal: 'required',
            account_type: 'required'
        },

        messages:{

        },

        submitHandler: function(form) {
            form.submit();
        },
    
    });

});