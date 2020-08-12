$(document).ready(function(){
    //Ingredients
    let ingredMax = 25; //Max no. ingredients
    const ingredHTML = '<div><input name="ingredients" type="text" class="form-control add-ingredient"></div>'; //New ingredient input field html 
    let x = 1; //Initial ingredient counter
    
    //Method steps
    let methodMax = 25; //Max no. method steps
    const methodHTML = '<div><input name="method" type="text" class="form-control add-method"></div>'; //New method input field html
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