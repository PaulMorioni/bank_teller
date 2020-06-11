$(function() {
    let initTellerBalance = htmlToFloat($('#initTellerBalance').html()); //Teller Balance from server
    let initBalanceFormArray = getTellerBalanceForm(); //Balance form from server
    newBalance = calculateTellerBalance(initBalanceFormArray, initTellerBalance);
    formattedTellerBal = formatBalance(newBalance);
    $('#tellerBalance').html(formattedTellerBal);

    $('.balanceFormField').change(function () {
        let balanceFormArray =  getTellerBalanceForm() 
        let newBalance = calculateTellerBalance(balanceFormArray, initTellerBalance)
        formattedTellerBal = formatBalance(newBalance);
        $('#tellerBalance').html(formattedTellerBal);
        
    });
    
    function createTellerBalance (floatBalance, stringBalance) {
        let newTellerBalance = {
            floatBalance : floatBalance,
            stringBalance : stringBalance
        };
        return newTellerBalance
    };

    function createNewBalanceEntry (elementId, elementValue, divider) {
        let elementValueFlt
        
        if (typeof elementValue == 'number'){       //validates type of elementValue
             elementValueFlt = elementValue
            elementValue = (elementValue).toFixed(2);
        } else if (typeof elementValue == 'string') {
            elementValueFlt = (elementValue).replace(',', '')
            elementValueFlt = parseFloat(elementValueFlt)
        };

        let newEntry = {
            elementId : elementId,
            elementValue : elementValue,
            elementFloat : elementValueFlt,
            divider : divider
        };
        return newEntry
    };

    function getTellerBalanceForm() {   //moves through each element and logs value as an array of objects
        let dividers = [100,1000,50,1000,20,500,10,100,5,100,2,100,1,100,1,25,.50,10,.25,10,.10,5,.05,2,.01,.50]
        balanceFormArray = []
        $('.balanceFormField').each( function (indexInArray, valueOfElement) {
            let elementId = $(this).attr('id');
            let elementValue = $(this).val();
            let elementDivider = dividers[indexInArray]
            elementValue = (elementValue).replace(',', '')

            if (['0',''].includes((elementValue).trim()) || isNaN(elementValue)) {   //checks for empty form and fills with zeros
                elementValue = '0.00'
                $(this).val(elementValue)
            } else {
                elementValue = closestWholeNumber(elementValue, elementDivider)
                $(this).val(elementValue)
            };
            if (!elementValue.includes('.')){
                elementValue = elementValue + '.00'
                $(this).val(elementValue)
            };
            let balanceFormEntry = createNewBalanceEntry(elementId, elementValue, elementDivider);

            balanceFormArray.push(balanceFormEntry);
        });//end for loop
        return balanceFormArray
    };

    function calculateTellerBalance(formArray, initTellerBalance){ //initTellerBalance used so calculations are absolute.
        let totalBalanced
        for (let index = 0; index < formArray.length; index++) {
            const elementObj = formArray[index];
            if ( index < 1) {
                totalBalanced = elementObj.elementFloat
            } else {
                totalBalanced = totalBalanced + elementObj.elementFloat
            }
        }//end for loop
        let newTellerBalanceFlt = totalBalanced - initTellerBalance
        return newTellerBalanceFlt
    }; //end calcTellerBalance

    function getTellerBalance(){
        let currentTellerCashStrVal = $('#tellerBalance').html();
        let currentTellerCashFltVal = htmlToFloat(currentTellerCashStrVal);
        tellerBalance = createTellerBalance(currentTellerCashFltVal, currentTellerCashStrVal);

        return tellerBalance

    };  //end teller balance constructor

    function formatBalance(tellerBalanceFlt){
        tellerBalanceFlt = (tellerBalanceFlt).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        tellerBalanceFlt = '$' + tellerBalanceFlt
        return tellerBalanceFlt
    };

    function htmlToFloat(htmlValue){
        htmlValue = htmlValue.replace('$', '');  //removes $ from str
        htmlValue = htmlValue.replace(',', ''); //removes comma so formatted str wont return leading 2 numbers
        htmlValue = htmlValue.trim();   //removes whitespace for float formatting
        htmlValue = parseFloat(htmlValue);
        return htmlValue
    };

    function closestWholeNumber(elementValue, divider){
        elementValue = parseFloat(elementValue);
        elementValue = (Math.round(elementValue/divider) * divider);
        elementValue = (elementValue).toFixed(2);
        elementValue = (elementValue).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        return elementValue
    };

    function formatOnSubmit(elementObjArray){   //needs to be fixed to properly format before storing
        for (let index = 0; index < elementObjArray.length; index++) {
            const elementObj = elementObjArray[index];
            let newElementValue = elementObj.elementValue
            newElementValue = newElementValue.replace(',','');
            newElementValue = newElementValue.replace('.00','');
            $('#' + elementObj.elementId).val(newElementValue)
        }
    };

    $('#submit').click(function () { 
        let newBalance = getTellerBalance()
        formatOnSubmit(getTellerBalanceForm());
        if (newBalance.floatBalance > 0 ) {
            alert("You're long")

        } else if (newBalance.floatBalance < 0) {
            alert("You're short")

        } else if (newBalance.floatBalance = 0) {
            alert('Congrats you balanced')
        };
        
    });
    
}); //close doc ready statement
