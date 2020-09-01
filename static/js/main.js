/*Functions to add and remove form input fields
 Adapted from this tutorial https://www.codexworld.com/add-remove-input-fields-dynamically-using-jquery/*/

$(document).ready(function(){
    //Ingredients
    let ingredMax = 25; //Max no. ingredients
    const ingredHTML = '<div><input name="ingredients" type="text" class="recipe-input form-control add-ingredient"></div>'; //New ingredient input field html 
    let x = 1; //Initial ingredient counter
    
    //Method steps
    let methodMax = 25; //Max no. method steps
    const methodHTML = '<div><input name="method" type="text" class="recipe-input form-control add-method"></div>'; //New method input field html
    let y = 1; //Initial method counter 

    //Button click to add ingredient field
    $('.add_ingred').click(function(){
        //Check maximum number of input fields
        if(x < ingredMax){ 
            x++; //Increment ingredient counter
            $('.ingredient-wrapper').append(ingredHTML); //Add ingredient field html
        }
    });
    
    //Button click to remove ingredient field
    $('.remove_ingred').click(function(){
        
        $('.add-ingredient').last().remove(); 
        x--; //Decrement ingredient counter
    });

    //Button click to add method field
    $('.add_step').click(function(){
        //Check maximum number of input fields
        if(y < methodMax){ 
            y++; //Increment method counter
            $('.method-wrapper').append(methodHTML); //Add method field html
        }
    });
    
    //Button click to remove method field
    $('.remove_step').click(function(){
        
        $('.add-method').last().remove(); 
        y--; //Decrement method counter
    });
});


/*Bootstrap custom form validation, taken from docs 
    https://getbootstrap.com/docs/4.0/components/forms/#how-it-works  */

(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    let forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    let validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

