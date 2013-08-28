$('input').autocomplete({
    minLength:3,
    source: function(req, add){
        $.ajax({
            url: '/ajax/url/',
            async: false,
            dataType:'json',
            type:'POST',
            data: {
                start: function() { return $(this).val(); },
            },
            success: function(data) {
 
                //create array for response objects
                var suggestions = [];
 
                //process response
                $.each(data.items, function(i, val){
                    suggestions.push(val[0]);
                });
 
                //pass array to callback
                add(suggestions);
            }
        });
    }
});